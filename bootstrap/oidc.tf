# GitHub Actions exchanges a short-lived OIDC token for temporary AWS
# credentials, so the repository stores no AWS access keys.
# AWS validates GitHub's certificate chain itself, so no thumbprint is pinned.

data "aws_caller_identity" "current" {}

data "aws_partition" "current" {}

resource "aws_iam_openid_connect_provider" "github" {
  count = var.create_oidc_provider ? 1 : 0

  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}

data "aws_iam_openid_connect_provider" "github" {
  count = var.create_oidc_provider ? 0 : 1

  url = "https://token.actions.githubusercontent.com"
}

locals {
  oidc_provider_arn = var.create_oidc_provider ? aws_iam_openid_connect_provider.github[0].arn : data.aws_iam_openid_connect_provider.github[0].arn

  account_id = data.aws_caller_identity.current.account_id
  partition  = data.aws_partition.current.partition

  # Exact OIDC subject claims. GitHub sets "sub" to:
  #   repo:OWNER/REPO:pull_request              for pull_request runs
  #   repo:OWNER/REPO:ref:refs/heads/main       for runs on main without an environment
  #   repo:OWNER/REPO:environment:NAME          for jobs that declare an environment
  plan_subjects = [
    "repo:${var.github_repository}:pull_request",
    "repo:${var.github_repository}:ref:refs/heads/main",
  ]
  apply_subjects = [
    "repo:${var.github_repository}:environment:${var.apply_environment}",
  ]

  # Exact state objects (must match "key" in backend.tf and
  # monitoring/terraform/backend.tf) plus the lock file Terraform writes
  # beside each one.
  state_keys = [
    "advanced-orchestration/root.tfstate",
    "advanced-orchestration/monitoring.tfstate",
  ]
  state_object_arns = flatten([
    for key in local.state_keys : [
      "${aws_s3_bucket.state.arn}/${key}",
      "${aws_s3_bucket.state.arn}/${key}.tflock",
    ]
  ])
}
