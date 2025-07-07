resource "aws_sagemaker_model" "this" {
  name               = var.model_name
  execution_role_arn = var.execution_role_arn

  primary_container {
    image          = var.image
    model_data_url = var.model_data_url
  }
}

