# IAM SageMaker Module

Creates IAM role for SageMaker with permissions for S3, ECR, and CloudWatch.

## Usage
```hcl
module "iam_sagemaker" {
  source    = "./modules/iam_sagemaker"
  role_name = "sagemaker-execution-role"
}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| role_name | IAM role name | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| role_arn | ARN of the SageMaker IAM role |
