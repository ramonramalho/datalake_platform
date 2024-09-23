provider "aws" {
  region = "us-east-2"
}

# # VPC
# resource "aws_vpc" "airflow_vpc" {
#   cidr_block = "10.0.0.0/16"
# }

# # Subnet
# resource "aws_subnet" "airflow_subnet" {
#   vpc_id            = aws_vpc.airflow_vpc.id
#   cidr_block        = "10.0.1.0/24"
#   availability_zone = "us-east-2a"
# }