# Plans the root stack against a mocked AWS provider: no credentials, no state,
# no cost. Catches plan-time failures that `terraform validate` cannot see,
# e.g. file functions on files that only exist after a local build.
# Run: terraform init -backend=false && terraform test

mock_provider "aws" {
  mock_data "aws_availability_zones" {
    defaults = {
      names = ["us-east-2a", "us-east-2b"]
    }
  }

  mock_data "aws_iam_policy_document" {
    defaults = {
      json = "{\"Version\":\"2012-10-17\",\"Statement\":[]}"
    }
  }
}

run "plans_on_clean_checkout" {
  command = plan

  assert {
    condition     = module.lambda.function_name == "my_lambda_function"
    error_message = "Lambda function should be planned from the Terraform-built package"
  }

  assert {
    condition     = data.archive_file.lambda.output_base64sha256 != ""
    error_message = "Lambda package hash should come from archive_file"
  }
}
