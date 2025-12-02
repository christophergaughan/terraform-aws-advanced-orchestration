# IAM Lambda Module

Creates IAM role and policy for Lambda execution with least-privilege permissions.

## Usage
```hcl
module "iam_lambda" {
  source      = "./modules/iam_lambda"
  role_name   = "lambda-execution-role"
  policy_json = data.aws_iam_policy_document.lambda_basic.json
}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| role_name | IAM role name | `string` | yes |
| policy_json | JSON policy document | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| role_arn | ARN of the IAM role |
| role_name | Name of the IAM role |
