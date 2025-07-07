provider "aws" {
  region = "us-east-1"
}

# call EventBridge module

module "eventbridge" {
  source              = "./modules/eventbridge"
  name                = "trigger-lambda-rule"
  description         = "Periodic trigger for Lambda function"
  schedule_expression = "rate(5 minutes)"
}

lambda_function_arn  = module.lambda.lambda_arn
lambda_function_name = module.lambda.function_name


# lambda module

module "lambda" {
  source         = "./modules/lambda"
  function_name  = "my_lambda_function"
  role_arn       = "arn:aws:iam::123456789012:role/lambda-execution-role" # replace with your actual role later
  filename       = "lambda_function_payload.zip" # stub for now
}


# SageMaker module

module "sagemaker" {
  source            = "./modules/sagemaker"
  model_name        = "my-sagemaker-model"
  execution_role_arn = "arn:aws:iam::123456789012:role/sagemaker-execution-role" # replace later
  image             = "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-sagemaker-image:latest"
  model_data_url    = "s3://my-model-bucket/model.tar.gz"
}


