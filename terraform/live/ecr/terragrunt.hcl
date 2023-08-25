locals {
  env = yamldecode(file(find_in_parent_folders("env.yml")))
  iam_role = "arn:aws:iam::${get_aws_account_id()}:role/${local.env.iam_role}"
}

iam_role = local.iam_role

include "root" {
  path = find_in_parent_folders()
}

include "generate_blocks" {
  path = "../_env/generate_blocks.hcl"
}

terraform {
  source = "tfr:///terraform-aws-modules/ecr/aws//?version=${local.env.ecr.module_version}"
}

inputs = {
    repository_name        = local.env.name
    repository_lifecycle_policy = jsonencode({
      rules = [
        {
          rulePriority = 1,
          description  = "Keep last 3 images",
          selection = {
            tagStatus     = "any",
            countType     = "imageCountMoreThan",
            countNumber   = 3
          },
          action = {
            type = "expire"
          }
        }
      ]
    })
}
