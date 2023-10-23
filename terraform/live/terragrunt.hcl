terragrunt_version_constraint = "~> 0.52.4"

remote_state {
  backend = "s3"
  config = {
    bucket         = "${get_aws_account_id()}-trade-bot-tf-state-bucket"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "trade-bot-tf-state-lock-table"
  }
}
