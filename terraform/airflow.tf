# Security Group
resource "aws_security_group" "airflow_sg" {
#   vpc_id = aws_vpc.airflow_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Permitir SSH de qualquer lugar
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Permitir acesso ao Airflow de qualquer lugar
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Par de Chaves (SSH)
resource "aws_key_pair" "airflow_key" {
  key_name   = "airflow-key"
  public_key = file(var.public_key_path)
}

# EC2 Instance
resource "aws_instance" "airflow_instance" {
  ami           = "ami-003932de22c285676"  # AMI do Ubuntu 20.04 LTS
  instance_type = "t2.large"
  associate_public_ip_address = true
  
#   subnet_id     = aws_subnet.airflow_subnet.id
  key_name      = aws_key_pair.airflow_key.key_name
  security_groups = [aws_security_group.airflow_sg.name]

  # user_data = file("bash.sh")  # Executa o script de instalação do Airflow

  tags = {
    Name = "Airflow-EC2"
  }
}

# Output do endereço público da instância
output "ec2_public_ip" {
  value = aws_instance.airflow_instance.public_ip
}

output "ec2_public_dns" {
  value = aws_instance.airflow_instance.public_dns
}
