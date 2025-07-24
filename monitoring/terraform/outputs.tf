output "grafana_workspace_url" {
  description = "URL of the Grafana workspace"
  value       = aws_grafana_workspace.monitoring.endpoint
}

output "prometheus_workspace_id" {
  description = "ID of the Prometheus (AMP) workspace"
  value       = aws_prometheus_workspace.monitoring.workspace_id
}

