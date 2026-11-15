variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_count" {
  description = "Number of public subnets to create"
  type        = number
  default     = 2
}


variable "availability_zones" {
  description = "Explicit list of availability zone names to place subnets in. Pinned rather than discovered so that subnet-to-AZ mapping stays stable across applies."
  type        = list(string)
  default     = ["us-east-2a", "us-east-2b", "us-east-2c"]
}
