locals {
  env = yamldecode(file(find_in_parent_folders("env.yml")))
  iam_role = "arn:aws:iam::${get_aws_account_id()}:role/${local.env.iam_role}"

  cidr           = "172.30.0.0/16"
  subnets        = cidrsubnets(local.cidr, 4, 4, 4)
  public_subnets = slice(local.subnets, 0, 3)
}

iam_role = local.iam_role

include "root" {
  path = find_in_parent_folders()
}

include "generate_blocks" {
  path = "../_env/generate_blocks.hcl"
}

terraform {
  source = "tfr:///terraform-aws-modules/vpc/aws//?version=${local.env.vpc.module_version}"
}

inputs = {
  name = local.env.name
  cidr = local.cidr

  azs             = ["us-east-1a", "us-east-1c", "us-east-1d"]
  public_subnets  = local.public_subnets

  enable_nat_gateway      = false
  enable_vpn_gateway      = false
  map_public_ip_on_launch = false
}
