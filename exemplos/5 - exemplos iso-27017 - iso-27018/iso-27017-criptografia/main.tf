# ISO 27017 - Controle de Criptografia de Dados em Nuvem
# Objetivo: Garantir criptografia em repouso e em trânsito para dados sensíveis

resource "aws_kms_key" "dados_sensiveis" {
  description             = "Chave KMS para criptografia de dados sensíveis - ISO 27017"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Compliance = "ISO-27017"
    Control    = "Criptografia"
  }
}

resource "aws_s3_bucket" "dados_conformidade" {
  bucket = "empresa-dados-conformidade-iso27017"

  tags = {
    Compliance = "ISO-27017"
    Control    = "Criptografia"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "criptografia" {
  bucket = aws_s3_bucket.dados_conformidade.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.dados_sensiveis.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "bloqueio_publico" {
  bucket = aws_s3_bucket.dados_conformidade.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
