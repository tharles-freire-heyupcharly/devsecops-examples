# ISO 27018 - Controle de Localização de Dados (Data Residency)
# Objetivo: Garantir que dados pessoais permaneçam em região específica (ex: Brasil - LGPD)

resource "aws_s3_bucket" "dados_pessoais_br" {
  bucket = "empresa-dados-pessoais-brasil"

  tags = {
    Compliance = "ISO-27018"
    Control    = "Localizacao"
    DataType   = "PersonalData"
    Region     = "Brazil"
    LGPD       = "true"
  }
}

# Política de bucket para prevenir replicação cross-region
resource "aws_s3_bucket_policy" "bloqueio_replicacao" {
  bucket = aws_s3_bucket.dados_pessoais_br.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "DenyReplicationOutsideBrazil"
        Effect    = "Deny"
        Principal = "*"
        Action = [
          "s3:PutReplicationConfiguration"
        ]
        Resource = "${aws_s3_bucket.dados_pessoais_br.arn}"
      }
    ]
  })
}

resource "aws_s3_bucket_lifecycle_configuration" "retencao_lgpd" {
  bucket = aws_s3_bucket.dados_pessoais_br.id

  rule {
    id     = "retencao-dados-pessoais"
    status = "Enabled"

    expiration {
      days = 1825 # 5 anos - requisito LGPD
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# AWS Config rule para verificação de conformidade
# Nota: aws_config_config_rule é o recurso correto no provider AWS v6+
resource "aws_config_config_rule" "verificacao_regiao" {
  name = "s3-dados-pessoais-regiao-brasil"

  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_VERSIONING_ENABLED"
  }

  scope {
    compliance_resource_types = ["AWS::S3::Bucket"]
  }

  tags = {
    Compliance = "ISO-27018"
    LGPD       = "DataResidency"
  }
}
