variable "function_name" {
  description = "Lambda function name"
  type        = string
}

variable "role_arn" {
  description = "IAM role ARN for Lambda"
  type        = string
}

variable "filename" {
  description = "Path to deployment package zip"
  type        = string
}

# subnets

variable "subnet_ids" {
  description = "Subnet IDs for Lambda VPC config"
  type        = list(string)
  default     = []
}

variable "security_group_ids" {
  description = "Security group IDs for Lambda VPC config"
  type        = list(string)
  default     = []
}


