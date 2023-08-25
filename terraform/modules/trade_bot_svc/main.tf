data "aws_region" "current" {}

#################
#### Service ####
#################
resource "aws_ecs_service" "this" {
  name          = var.name
  cluster       = var.ecs_cluster_id
  desired_count = 1
  launch_type   = "FARGATE"

  task_definition = "${aws_ecs_task_definition.this.family}:${aws_ecs_task_definition.this.revision}"

  network_configuration {
    assign_public_ip = true
    security_groups = [aws_security_group.ecs_service.id]
    subnets         = var.subnet_ids
  }
}

#######################
### Task Definition ###
#######################
resource "aws_ecs_task_definition" "this" {
  family                   = var.name
  task_role_arn            = aws_iam_role.task_role.arn
  execution_role_arn       = aws_iam_role.task_execution.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.ecs_vcpu
  memory                   = var.ecs_memory
  container_definitions = jsonencode([
    {
      "name" = var.name,
      "image" = "${var.ecr_repo}:${var.image_tag}",
      "portMappings" = [],
      "environment" = [],
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
