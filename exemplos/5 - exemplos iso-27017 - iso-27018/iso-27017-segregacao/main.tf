# ISO 27017 - Controle de Segregação de Ambientes em Nuvem
# Objetivo: Isolar ambientes de desenvolvimento, teste e produção

resource "aws_vpc" "producao" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name       = "VPC-Producao"
    Compliance = "ISO-27017"
    Control    = "Segregacao"
    Environment = "production"
  }
}

resource "aws_vpc" "desenvolvimento" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name       = "VPC-Desenvolvimento"
    Compliance = "ISO-27017"
    Control    = "Segregacao"
    Environment = "development"
  }
}

resource "aws_subnet" "producao_privada" {
  vpc_id            = aws_vpc.producao.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name        = "Subnet-Producao-Privada"
    Environment = "production"
    Compliance  = "ISO-27017"
  }
}

resource "aws_subnet" "dev_privada" {
  vpc_id            = aws_vpc.desenvolvimento.id
  cidr_block        = "10.1.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name        = "Subnet-Dev-Privada"
    Environment = "development"
    Compliance  = "ISO-27017"
  }
}

resource "aws_network_acl" "producao_acl" {
  vpc_id = aws_vpc.producao.id

  # Bloqueia tráfego entre VPCs
  egress {
    protocol   = "-1"
    rule_no    = 100
    action     = "deny"
    cidr_block = aws_vpc.desenvolvimento.cidr_block
    from_port  = 0
    to_port    = 0
  }

  tags = {
    Name       = "ACL-Producao-Segregacao"
    Compliance = "ISO-27017"
  }
}
