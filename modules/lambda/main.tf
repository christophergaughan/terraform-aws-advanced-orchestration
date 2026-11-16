# X-Ray tracing is an optional observability feature for this demo; the same
# decision is recorded for Checkov as CKV_AWS_50 in .checkov.yml.
#tfsec:ignore:aws-lambda-enable-tracing
resource "aws_lambda_function" "this" {
  function_name    = var.function_name
  role             = var.role_arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  filename         = var.filename
  source_code_hash = var.source_code_hash

  environment {
    variables = {
      SAGEMAKER_ENDPOINT_NAME = var.sagemaker_endpoint_name
    }
  }
}

output "lambda_arn" {
  value = aws_lambda_function.this.arn
}

output "function_name" {
  value = aws_lambda_function.this.function_name
}
