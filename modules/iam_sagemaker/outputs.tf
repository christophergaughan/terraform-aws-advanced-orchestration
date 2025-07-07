output "role_arn" {
  description = "ARN of the SageMaker execution role"
  value       = aws_iam_role.this.arn
}

