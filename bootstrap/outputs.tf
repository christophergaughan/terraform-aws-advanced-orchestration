output "state_bucket" {
  description = "S3 bucket for Terraform state; set as the GitHub variable TF_STATE_BUCKET"
  value       = aws_s3_bucket.state.bucket
}

output "plan_role_arn" {
  description = "Role for terraform plan; set as the GitHub secret AWS_PLAN_ROLE_ARN"
  value       = aws_iam_role.plan.arn
}

output "apply_role_arn" {
  description = "Role for approval-gated apply/destroy; set as the GitHub secret AWS_APPLY_ROLE_ARN"
  value       = aws_iam_role.apply.arn
}

output "region" {
  description = "Region the state bucket lives in"
  value       = var.region
}
