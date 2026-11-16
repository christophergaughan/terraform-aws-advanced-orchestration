# Monitoring Stack – Prometheus & Grafana (AWS Managed)

This folder configures the observability layer for the orchestration platform:
- Amazon Managed Service for Prometheus (AMP) for metric storage
- Amazon Managed Grafana for visualization
- An IAM role that lets Grafana read from Prometheus

State is stored in the shared S3 state bucket under
`advanced-orchestration/monitoring.tfstate` (see `backend.tf`).

## Prerequisite

Grafana here authenticates with `AWS_SSO`, which requires **IAM Identity Center**
to be enabled in the AWS account. Without it, creating the Grafana workspace fails.

## Deploy (recommended: from CI)

Actions → **Terraform Apply / Destroy** → Run workflow → stack `monitoring`,
action `apply`. Review the plan in the run summary, then approve the
`aws-apply` environment. Use action `destroy` to tear it down the same way.

## Deploy from your machine

```bash
cd monitoring/terraform
terraform init -backend-config="bucket=$(terraform -chdir=../../bootstrap output -raw state_bucket)"
terraform plan
terraform apply
```

## Check without AWS access

```bash
terraform init -backend=false && terraform validate && terraform test
```

