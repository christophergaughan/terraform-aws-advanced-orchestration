# Remote state for the monitoring stack (same bucket as the root stack,
# separate key). Supply the bucket at init time:
#
#   terraform init -backend-config="bucket=<state bucket>"
terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    key          = "advanced-orchestration/monitoring.tfstate"
    region       = "us-east-2"
    encrypt      = true
    use_lockfile = true
  }
}
