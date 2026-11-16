provider "aws" {
  region = "us-east-2"
}

# VPC module
module "vpc" {
  source              = "./modules/vpc"
  vpc_cidr            = "10.0.0.0/16"
  public_subnet_count = 1
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

locals {
  lambda_function_name    = "my_lambda_function"
  sagemaker_endpoint_name = "my-sagemaker-endpoint"

  account_id           = data.aws_caller_identity.current.account_id
  region               = data.aws_region.current.region
  lambda_log_group_arn = "arn:aws:logs:${local.region}:${local.account_id}:log-group:/aws/lambda/${local.lambda_function_name}"
}

# IAM Lambda module - least privilege: this function's own log group and the
# one endpoint it calls, in this account and region only.
data "aws_iam_policy_document" "lambda_basic" {
  statement {
    actions   = ["logs:CreateLogGroup"]
    resources = [local.lambda_log_group_arn]
  }
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    # Lambda names its log streams at runtime, so the stream segment is "*"
    # inside this function's log group.
    #tfsec:ignore:aws-iam-no-policy-wildcards
    resources = ["${local.lambda_log_group_arn}:log-stream:*"]
  }
  statement {
    actions   = ["sagemaker:InvokeEndpoint"]
    resources = ["arn:aws:sagemaker:${local.region}:${local.account_id}:endpoint/${local.sagemaker_endpoint_name}"]
  }
}

module "iam_lambda" {
  source      = "./modules/iam_lambda"
  role_name   = "lambda-execution-role"
  policy_json = data.aws_iam_policy_document.lambda_basic.json
}

# Lambda deployment package, built by Terraform from source so plan works on
# a clean checkout (CI) without a pre-built, gitignored zip. boto3 ships in the
# Lambda Python runtime, so the handler file is the whole package.
data "archive_file" "lambda" {
  type        = "zip"
  source_file = "${path.module}/lambda_function/lambda_function.py"
  output_path = "${path.module}/lambda_function_payload.zip"
}

# Lambda module
module "lambda" {
  source                  = "./modules/lambda"
  function_name           = local.lambda_function_name
  role_arn                = module.iam_lambda.role_arn
  filename                = data.archive_file.lambda.output_path
  source_code_hash        = data.archive_file.lambda.output_base64sha256
  sagemaker_endpoint_name = local.sagemaker_endpoint_name
}

# EventBridge module
module "eventbridge" {
  source               = "./modules/eventbridge"
  name                 = "trigger-lambda-rule"
  description          = "Periodic trigger for Lambda function"
  schedule_expression  = "rate(5 minutes)"
  lambda_function_arn  = module.lambda.lambda_arn
  lambda_function_name = module.lambda.function_name
}

# SageMaker module
module "sagemaker" {
  source             = "./modules/sagemaker"
  model_name         = "my-sagemaker-model"
  execution_role_arn = "arn:aws:iam::123456789012:role/sagemaker-execution-role"
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
