# Monitoring Stack – Prometheus & Grafana (AWS Managed)

This folder configures the observability layer for the orchestration platform using:
-  Amazon Managed Service for Prometheus (AMP)
-  Amazon Managed Grafana
-  EKS/ECS service metric scraping

## Setup

```
cd monitoring/terraform
warp terraform init
warp terraform apply
```

# Monitoring Stack (Terraform Module)

This Terraform stack sets up:
-  Amazon Managed Prometheus (AMP) for metric storage
-  Amazon Managed Grafana for visualization
-  IAM role to allow Grafana access to Prometheus

##  Usage

From inside this directory:

```
warp terraform init
warp terraform apply
```

# Triggered on Tue Jul 29 14:46:50 EDT 2025
