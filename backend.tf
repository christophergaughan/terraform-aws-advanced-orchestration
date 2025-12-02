# Remote State Configuration
# Uncomment for production use with S3 backend + DynamoDB locking
#
# terraform {
#   backend "s3" {
#     bucket         = "your-terraform-state-bucket"
#     key            = "advanced-orchestration/terraform.tfstate"
#     region         = "us-east-2"
#     encrypt        = true
#     dynamodb_table = "terraform-state-lock"
#   }
# }
