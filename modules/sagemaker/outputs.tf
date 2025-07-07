output "sagemaker_model_arn" {
  description = "ARN of the SageMaker model"
  value       = aws_sagemaker_model.this.arn
}

