# Plans the monitoring stack against a mocked AWS provider (no credentials).
# Run from monitoring/terraform: terraform init -backend=false && terraform test

mock_provider "aws" {}

run "plans_monitoring_stack" {
  command = plan

  assert {
    condition     = aws_prometheus_workspace.monitoring.alias == "orchestration-metrics"
    error_message = "AMP workspace alias changed"
  }

  assert {
    condition     = contains(aws_grafana_workspace.monitoring.authentication_providers, "AWS_SSO")
    error_message = "Grafana should authenticate through IAM Identity Center"
  }
}
