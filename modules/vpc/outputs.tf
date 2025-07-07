output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.this.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "batch_subnet_id" {
  value = aws_subnet.batch_private.id
}

output "realtime_subnet_id" {
  value = aws_subnet.realtime_private.id
}

output "public_subnet_id" {
  value = aws_subnet.public.id
}

