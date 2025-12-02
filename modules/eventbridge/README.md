# EventBridge Module

Creates EventBridge rules to trigger Lambda functions on schedule or event patterns.

## Usage
```hcl
module "eventbridge" {
  source               = "./modules/eventbridge"
  name                 = "ml-pipeline-trigger"
  description          = "Triggers ML preprocessing every 5 minutes"
  schedule_expression  = "rate(5 minutes)"
  lambda_function_arn  = module.lambda.lambda_arn
  lambda_function_name = module.lambda.function_name
}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| name | Rule name | `string` | yes |
| description | Rule description | `string` | yes |
| schedule_expression | Cron or rate expression | `string` | yes |
| lambda_function_arn | Target Lambda ARN | `string` | yes |
| lambda_function_name | Target Lambda name | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| rule_arn | ARN of the EventBridge rule |
