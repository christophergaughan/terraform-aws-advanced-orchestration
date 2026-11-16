# Bootstrap stack: run ONCE from your own machine, before any CI workflow
# can talk to AWS. It creates the pieces every other stack depends on:
#   - the S3 bucket that holds Terraform state for the root and monitoring stacks
#   - the GitHub Actions OIDC identity provider (no long-lived AWS keys in GitHub)
#   - a read-only "plan" role and an approval-gated "apply" role
#
# This stack keeps LOCAL state (bootstrap/terraform.tfstate, gitignored),
# because it creates the bucket the other stacks store their state in.
# Keep that file, or move it into the bucket afterwards (see README.md).

terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Project   = "terraform-aws-advanced-orchestration"
      ManagedBy = "terraform-bootstrap"
    }
  }
}
