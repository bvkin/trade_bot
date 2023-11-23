variable "name" {
  description = "Name of service"
  type        = string
}

variable "vpc_id" {
  description = "Id of VPC in which to deploy resoruces"
  type        = string
}

variable "subnet_ids" {
  description = "Ids of subnets in which to deploy services"
  type        = list(string)
}

variable "ecs_cluster_id" {
  description = "Cluster id in which to deploy ECS resources"
  type        = string
}

variable "ecr_repo" {
  description = "Specify ecr repo from which container should be pulled"
  type        = string
}

variable "image_tag" {
  description = "Tag of image to deploy"
  type        = string
  default     = "latest"
}

variable "ecs_vcpu" {
  description = "Vcpu value assigned to ECS cluster"
  type        = number
  default     = 256
}

variable "ecs_memory" {
  description = "Memory value assigned to ECS cluster"
  type        = number
  default     = 512
}

variable "sns_topic_arn" {
  description = "SNS topic arn for publishing messages"
  type = string
}

variable "strategy" {
  description = "Trading strategy to use for evaluating tickers"
  type = string
}

variable "tickers" {
  description = "A list of stock tickers on which the trade bot should trade"
  type = list(string)
}
