# SageMaker Module

Provisions SageMaker model and endpoint for ML inference.

## Usage
```hcl
module "sagemaker" {
  source             = "./modules/sagemaker"
  model_name         = "glycosylation-scanner"
  execution_role_arn = module.iam_sagemaker.role_arn
  image              = "123456789012.dkr.ecr.us-east-1.amazonaws.com/model:latest"
  model_data_url     = "s3://models-bucket/model.tar.gz"
}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| model_name | SageMaker model name | `string` | yes |
| execution_role_arn | IAM role for SageMaker | `string` | yes |
| image | ECR image URI | `string` | yes |
| model_data_url | S3 path to model artifacts | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| model_arn | ARN of the SageMaker model |
| endpoint_name | Name of the inference endpoint |
