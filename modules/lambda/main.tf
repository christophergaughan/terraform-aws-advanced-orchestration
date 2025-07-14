resource "aws_lambda_function" "this" {
  function_name    = var.function_name
  role             = var.role_arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  filename         = var.filename
  source_code_hash = filebase64sha256(var.filename)

  environment {
    variables = {
      SAGEMAKER_ENDPOINT_NAME = "my-sagemaker-endpoint" # update if needed
    }
  }

  # Optional VPC config if using VPC
  # vpc_config {
  #   subnet_ids         = [module.vpc.realtime_subnet_id]
  #   security_group_ids = []
  # }
}

output "lambda_arn" {
  value = aws_lambda_function.this.arn
}

output "function_name" {
  value = aws_lambda_function.this.function_name
}

