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

dependency "vpc" {
  config_path = "${path_relative_from_include("root")}/vpc"
  mock_outputs = {
    vpc_id = "vpc-0123456789abcde"
    subnet_ids = ["subnet-0123456789abcde", "subnet-0123456789fghij", "subnet-0123456789klmno"]
  }
}

dependency "ecr" {
  config_path = "${path_relative_from_include("root")}/ecr"
  mock_outputs = {
    repository_url = "123456789101.dkr.ecr.us-east-1.amazonaws.com/trade_bot"
  }
}

dependency "ecs_cluster" {
  config_path = "${path_relative_from_include("root")}/ecs_cluster"
  mock_outputs = {
    cluster_id = local.env.name
  }
}

dependency "sns" {
  config_path = "${path_relative_from_include("root")}/sns"
  mock_outputs = {
    topic_arn = "arn:aws:sns:us-east-1:123456789012:trade_bot_signals"
  }
}

terraform {
  source = "${path_relative_from_include("root")}/../modules//trade_bot_svc"
}

inputs = {
    name = local.env.name
    vpc_id = dependency.vpc.outputs.vpc_id
    subnet_ids = dependency.vpc.outputs.public_subnets
    ecr_repo = dependency.ecr.outputs.repository_url
    ecs_cluster_id = dependency.ecs_cluster.outputs.cluster_id
    sns_topic_arn = dependency.sns.outputs.topic_arn
    strategy = "MovingAverages"
    tickers = [
      "ADP",
      "AFL",
      "BKR",
      "BKNG",
      "CAT",
      "COST",
      "KMB",
      "LIN",
      "NEE",
      "ROK"
    ]
}
