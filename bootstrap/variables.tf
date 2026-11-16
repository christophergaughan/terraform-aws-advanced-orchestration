variable "region" {
  description = "AWS region for the state bucket (must match the region in the stacks' backend blocks)"
  type        = string
  default     = "us-east-2"
}

variable "github_repository" {
  description = "GitHub repository allowed to assume the CI roles, as owner/name"
  type        = string
  default     = "christophergaughan/terraform-aws-advanced-orchestration"
}

variable "apply_environment" {
  description = "GitHub environment whose jobs may assume the apply role (protect it with a required reviewer)"
  type        = string
  default     = "aws-apply"
}

variable "create_oidc_provider" {
  description = "Create the GitHub OIDC provider. Set to false if this AWS account already has one for token.actions.githubusercontent.com (an account can only have one)."
  type        = bool
  default     = true
}

variable "state_bucket_prefix" {
  description = "Prefix for the state bucket name; a random suffix keeps it globally unique without putting the account ID in the name"
  type        = string
  default     = "tf-advanced-orchestration-state"
}

variable "noncurrent_state_retention_days" {
  description = "Days to keep superseded state versions (versioning is the undo button for a bad apply)"
  type        = number
  default     = 90
}
