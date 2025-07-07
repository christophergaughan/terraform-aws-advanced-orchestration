resource "aws_lambda_function" "this" {
  function_name    = var.function_name
  role             = var.role_arn
  handler          = "lambda_function.lambda_handler" # <- update to match  Python file
  runtime          = "python3.9"
  filename         = var.filename
  source_code_hash = filebase64sha256(var.filename)

  environment {
    variables = {
      SAGEMAKER_ENDPOINT_NAME = "my-sagemaker-endpoint" # Replace with real endpoint name later
    }
  }
}

