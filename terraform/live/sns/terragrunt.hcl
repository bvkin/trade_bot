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
  source = "tfr:///terraform-aws-modules/sns/aws//?version=${local.env.sns.module_version}"
}

inputs = {
  name  = "${local.env.name}_signals"

  subscriptions = {
    sms = {
      protocol = "sms"
      endpoint = "+19788285539"
    }
  }
}
