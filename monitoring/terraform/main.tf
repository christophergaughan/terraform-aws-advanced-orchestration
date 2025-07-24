provider "aws" {
  region = var.region
}

resource "aws_prometheus_workspace" "monitoring" {
  alias = "orchestration-metrics"
}

resource "aws_grafana_workspace" "monitoring" {
  name                     = "orchestration-monitoring"
  account_access_type      = "CURRENT_ACCOUNT"
  authentication_providers = ["AWS_SSO"]
  permission_type          = "SERVICE_MANAGED"
  role_arn                 = aws_iam_role.grafana_admin.arn
}

resource "aws_iam_role" "grafana_admin" {
  name = "grafana-admin-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "grafana.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "grafana_prometheus_access" {
  role       = aws_iam_role.grafana_admin.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonPrometheusFullAccess"
}

