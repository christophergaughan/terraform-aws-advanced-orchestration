# Pins the security-critical shape of the bootstrap stack against a mocked AWS
# provider (no credentials): who may assume which role, and which state
# objects the roles may touch. "apply" here runs entirely against the mock;
# nothing is created in AWS.
# Run from bootstrap/: terraform init && terraform test

mock_provider "aws" {
  mock_data "aws_partition" {
    defaults = {
      partition = "aws"
    }
  }

  mock_data "aws_caller_identity" {
    defaults = {
      account_id = "111111111111"
    }
  }

  mock_data "aws_iam_policy_document" {
    defaults = {
      json = "{\"Version\":\"2012-10-17\",\"Statement\":[]}"
    }
  }
}

run "trust_and_state_scope" {
  command = apply

  assert {
    condition = toset(local.apply_subjects) == toset([
      "repo:christophergaughan/terraform-aws-advanced-orchestration:environment:aws-apply",
    ])
    error_message = "Only the approval-gated aws-apply environment may assume the apply role"
  }

  assert {
    condition = toset(local.plan_subjects) == toset([
      "repo:christophergaughan/terraform-aws-advanced-orchestration:pull_request",
      "repo:christophergaughan/terraform-aws-advanced-orchestration:ref:refs/heads/main",
    ])
    error_message = "Plan role should be assumable only from pull requests and main"
  }

  assert {
    condition     = alltrue([for arn in local.state_object_arns : !strcontains(arn, "*")])
    error_message = "State access must list exact objects, not wildcards"
  }

  assert {
    condition     = length(local.state_object_arns) == 4
    error_message = "Expected two state files plus their two lock files"
  }

  assert {
    condition     = startswith(aws_s3_bucket.state.bucket, "tf-advanced-orchestration-state-")
    error_message = "State bucket name should use the prefix plus a random suffix"
  }
}
