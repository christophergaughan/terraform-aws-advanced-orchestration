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

variable "sagemaker_endpoint_name" {
  description = "SageMaker endpoint the function invokes (exposed as SAGEMAKER_ENDPOINT_NAME)"
  type        = string
  default     = "my-sagemaker-endpoint"
}

variable "source_code_hash" {
  description = "Base64 SHA-256 of the package (e.g. archive_file's output_base64sha256), so code changes trigger a redeploy. Passed in rather than computed here because the zip may not exist until plan time."
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


