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

# Updaste vars in EventBridge module

variable "lambda_function_arn" {
  description = "ARN of the Lambda function to target"
  type        = string
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
}


