# Remote State Configuration - S3 backend with native S3 state locking.
#
# The bucket is created once by ./bootstrap. Its name is supplied at init time
# so it stays out of this public repo:
#
#   terraform init -backend-config="bucket=<state bucket>"
#
# Locking: Terraform >= 1.10 writes a lock file next to the state object
# (use_lockfile). The older DynamoDB lock table is deprecated and not needed.
terraform {
  backend "s3" {
    key          = "advanced-orchestration/root.tfstate"
    region       = "us-east-2"
    encrypt      = true
    use_lockfile = true
  }
}
