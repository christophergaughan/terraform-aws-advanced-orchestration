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

# Create IAM  policy for Lambda

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
    resources = ["*"] # You can further restrict this later to specific SageMaker endpoint ARNs
  }
}

# Call IAM module

module "iam_lambda" {
  source      = "./modules/iam_lambda"
  role_name   = "lambda-execution-role"
  policy_json = data.aws_iam_policy_document.lambda_basic.json
}


# lambda module

module "lambda" {
  source         = "./modules/lambda"
  function_name  = "my_lambda_function"
  role_arn       = module.iam_lambda.role_arn
  file           = "lambda_function_payload.zip" #made payload 
}


# SageMaker module

module "sagemaker" {
  source            = "./modules/sagemaker"
  model_name        = "my-sagemaker-model"
  execution_role_arn = "arn:aws:iam::123456789012:role/sagemaker-execution-role" # replace later
  image             = "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-sagemaker-image:latest"
  model_data_url    = "s3://my-model-bucket/model.tar.gz"
}


