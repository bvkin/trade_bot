data "aws_region" "current" {}

#################
#### Service ####
#################
resource "aws_ecs_service" "this" {
  name          = var.name
  cluster       = var.ecs_cluster_id
  desired_count = 1
  launch_type   = "EC2"

  task_definition = "${aws_ecs_task_definition.this.family}:${aws_ecs_task_definition.this.revision}"
}

#######################
### Task Definition ###
#######################
resource "aws_ecs_task_definition" "this" {
  family                   = var.name
  task_role_arn            = aws_iam_role.task_role.arn
  execution_role_arn       = aws_iam_role.task_execution.arn
  requires_compatibilities = ["EC2"]
  cpu                      = var.ecs_vcpu
  memory                   = var.ecs_memory
  container_definitions = jsonencode([
    {
      "name" = var.name,
      "image" = "${var.ecr_repo}:${var.image_tag}",
      "portMappings" = [],
      "command": ["--strategy", var.strategy, "--tickers", join(",", var.tickers)],
      "environment" = [
        {
          name = "AWS_SNS_TOPIC_ARN"
          value = var.sns_topic_arn
        },
        {
          name = "AWS_DEFAULT_REGION"
          value = data.aws_region.current.name
        }
      ],
      "secrets" = [
        {
          name      = "ALPACA_API_KEY",
          valueFrom = aws_ssm_parameter.alpaca_api_key.arn
        },
        {
          name      = "ALPACA_SECRET_KEY",
          valueFrom = aws_ssm_parameter.alpaca_secret_key.arn
        }
      ]
      "logConfiguration" = {
        "logDriver" = "awslogs"
        "options" = {
          "awslogs-group" = "/aws/ecs/${var.name}",
          "awslogs-region" = data.aws_region.current.name,
          "awslogs-stream-prefix" = var.name
        }
      }
    }
  ])
}


###########
### EC2 ###
###########
data "aws_ssm_parameter" "ecs_optimized_ami" {
  name = "/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id"
}

resource "aws_instance" "this" {
  ami           =  data.aws_ssm_parameter.ecs_optimized_ami.value
  instance_type = var.ec2_instance_type

  associate_public_ip_address = true
  subnet_id                   = var.subnet_ids[0]
  vpc_security_group_ids      = [aws_security_group.ecs_service.id]

  user_data = <<-EOF
              #!/bin/bash
              echo ECS_CLUSTER=${var.ecs_cluster_id} >> /etc/ecs/ecs.config
              EOF

  iam_instance_profile = aws_iam_instance_profile.ecs_instance_profile.name
}

########################
#### Security Group ####
########################
resource "aws_security_group" "ecs_service" {
  vpc_id = var.vpc_id
  name   = "${var.name}-ecs-service"
}

resource "aws_security_group_rule" "egress_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 65535
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.ecs_service.id
}

#######################
### Parameter Store ###
#######################
resource "aws_ssm_parameter" "alpaca_api_key" {
  name  = "/${var.name}/alpaca_api_key"
  type  = "SecureString"
  value = "this"

  lifecycle {
    ignore_changes = [
      value
    ]
  }
}

resource "aws_ssm_parameter" "alpaca_secret_key" {
  name  = "/${var.name}/alpaca_secret_key"
  type  = "SecureString"
  value = "this"

  lifecycle {
    ignore_changes = [
      value
    ]
  }
}

#############
#### IAM ####
#############
# ECS Task Executuion Role
data "aws_iam_policy_document" "service_assume_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type = "Service"
      identifiers = [
        "ecs-tasks.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "task_execution" {
  name = "${var.name}_task_execution_role"

  assume_role_policy = data.aws_iam_policy_document.service_assume_policy.json
}

resource "aws_iam_role_policy_attachment" "task_execution" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


# ECS Task Role
resource "aws_iam_role" "task_role" {
  name               = "${var.name}_task_role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.task_role.json
}

data "aws_iam_policy_document" "task_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# Param Store
resource "aws_iam_policy" "param_store" {
  name   = "${var.name}_param_store"
  path   = "/"
  policy = data.aws_iam_policy_document.param_store.json
}

data "aws_iam_policy_document" "param_store" {
  statement {
    sid = "ParamStoreAccess"
    actions = [
      "ssm:GetParameters",
      "secretsmanager:GetSecretValue",
      "kms:Decrypt"
    ]
    resources = [
      aws_ssm_parameter.alpaca_api_key.arn,
      aws_ssm_parameter.alpaca_secret_key.arn
    ]
  }
}

resource "aws_iam_role_policy_attachment" "param_store" {
  role       = aws_iam_role.task_execution.name
  policy_arn = aws_iam_policy.param_store.arn
}

# EC2
resource "aws_iam_role" "ecs_instance_role" {
  name = "${var.name}_ecs_instance_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "ecs_instance_role_attachment" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_role_policy_attachment" "systems_manager" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedEC2InstanceDefaultPolicy"
}

resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "${var.name}_ecs_instance_profile"
  role = aws_iam_role.ecs_instance_role.name
}
