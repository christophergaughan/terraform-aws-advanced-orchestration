# VPC Module

Provisions a VPC with public subnets for Lambda and SageMaker networking.

## Usage
```hcl
module "vpc" {
  source              = "./modules/vpc"
  vpc_cidr            = "10.0.0.0/16"
  public_subnet_count = 2
}
```

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| vpc_cidr | CIDR block for VPC | `string` | yes |
| public_subnet_count | Number of public subnets | `number` | yes |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | ID of the VPC |
| public_subnet_ids | List of public subnet IDs |
