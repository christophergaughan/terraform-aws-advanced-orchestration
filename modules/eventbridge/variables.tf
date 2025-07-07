variable "name" {
  description = "Name of the EventBridge rule"
  type        = string
}

variable "description" {
  description = "Description of the rule"
  type        = string
  default     = "Trigger for Lambda"
}

variable "schedule_expression" {
  description = "Schedule expression (e.g., cron)"
  type        = string
}

