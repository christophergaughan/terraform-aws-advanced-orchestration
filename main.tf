data "aws_availability_zones" "available" {}

provider "aws" {
  region = "us-east-1"
}

# EventBridge module
module "eventbridge" {
  source              = "./modules/eventbridge"
  name                = "trigger-lambda-rule"
  description         = "Periodic trigger for Lambda function"
  schedule_expression = "rate(5 minutes)"
}

# IAM Lambda module
data "aws_iam_policy_document" "lambda_basic" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }

  statement {
    actions = [
      "sagemaker:InvokeEndpoint"
    ]
    resources = ["*"]
  }
}

module "iam_lambda" {
  source      = "./modules/iam_lambda"
  role_name   = "lambda-execution-role"
  policy_json = data.aws_iam_policy_document.lambda_basic.json
}

# VPC module
module "vpc" {
  source              = "./modules/vpc"
  vpc_cidr            = "10.0.0.0/16"
  public_subnet_count = 1
}

# Lambda module
module "lambda" {
  source        = "./modules/lambda"
  function_name = "my_lambda_function"
  role_arn      = module.iam_lambda.role_arn
  filename      = "lambda_function_payload.zip"
}

# SageMaker module
module "sagemaker" {
  source             = "./modules/sagemaker"
  model_name         = "my-sagemaker-model"
  execution_role_arn = "arn:aws:iam::123456789012:role/sagemaker-execution-role" # replace later
  image              = "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-sagemaker-image:latest"
  model_data_url     = "s3://my-model-bucket/model.tar.gz"
}

# Outputs
output "lambda_function_arn" {
  value = module.lambda.lambda_arn
}

output "lambda_function_name" {
  value = module.lambda.function_name
}


