# Configuração do Provider AWS
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

# Configuração da região AWS
provider "aws" {
  region = "us-east-1"
}

# Recurso: Volume EBS
resource "aws_ebs_volume" "web_server_storage" {
  availability_zone = "us-east-1a"
  size              = 20 # 20GB
  type              = "gp3"

  # Configurações de performance para GP3
  throughput = 125  # MB/s
  iops       = 3000 # IOPS

  # Criptografia
  encrypted = true

  tags = {
    Name        = "WebServer-Storage"
    Environment = "Development"
    Project     = "IaC-Demo"
    Owner       = "DevOps-Team"
  }
}

# Recurso: Instância EC2
resource "aws_instance" "web_server" {
  # AMI (Amazon Machine Image) - Ubuntu 22.04 LTS
  ami = "ami-0c7217cdde317cfec"

  # Tipo da instância
  instance_type = "t3.micro"

  # Availability Zone (deve ser a mesma do EBS)
  availability_zone = "us-east-1a"

  # Chave SSH para acesso
  key_name = "my-key-pair"

  # Security Group
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  # Tags para organização
  tags = {
    Name        = "WebServer-Terraform"
    Environment = "Development"
    Project     = "IaC-Demo"
    Owner       = "DevOps-Team"
  }
}

# Anexar o volume EBS à instância EC2
resource "aws_volume_attachment" "web_server_ebs_attachment" {
  device_name = "/dev/xvdf"
  volume_id   = aws_ebs_volume.web_server_storage.id
  instance_id = aws_instance.web_server.id

  # Não forçar detach quando destruir
  force_detach = false
}

# Security Group para a EC2
resource "aws_security_group" "web_sg" {
  name_prefix = "web-server-sg"
  description = "Security group for web server"

  # Regra de entrada - HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP access"
  }

  # Regra de entrada - SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Restrinja para seu IP em produção
    description = "SSH access"
  }

  # Regra de saída - Tudo
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }

  tags = {
    Name = "WebServer-SecurityGroup"
  }
}

# Outputs
output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.web_server.public_ip
}

output "instance_public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.web_server.public_dns
}

output "ebs_volume_id" {
  description = "ID of the EBS volume"
  value       = aws_ebs_volume.web_server_storage.id
}

output "ebs_volume_size" {
  description = "Size of the EBS volume in GB"
  value       = aws_ebs_volume.web_server_storage.size
}