variable "role_name" {
  description = "Name of the IAM role for SageMaker"
  type        = string
}

variable "policy_json" {
  description = "IAM policy JSON for SageMaker role"
  type        = string
}

