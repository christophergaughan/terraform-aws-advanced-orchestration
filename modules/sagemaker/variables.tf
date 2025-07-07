variable "model_name" {
  description = "Name of the SageMaker model"
  type        = string
}

variable "execution_role_arn" {
  description = "Execution role ARN for SageMaker"
  type        = string
}

variable "image" {
  description = "Container image URI"
  type        = string
}

variable "model_data_url" {
  description = "S3 location of model artifacts"
  type        = string
}

