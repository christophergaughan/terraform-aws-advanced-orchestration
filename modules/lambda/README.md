# Lambda Module

Deploys an AWS Lambda function with Python runtime for event-driven processing.

## Usage
```hcl
module "lambda" {
  source        = "./modules/lambda"
  function_name = "ml-preprocessor"
  role_arn      = module.iam_lambda.role_arn
  filename      = "lambda_payload.zip"
}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| function_name | Lambda function name | `string` | yes |
| role_arn | IAM execution role ARN | `string` | yes |
| filename | Path to deployment ZIP | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| lambda_arn | ARN of the Lambda function |
| function_name | Name of the Lambda function |
