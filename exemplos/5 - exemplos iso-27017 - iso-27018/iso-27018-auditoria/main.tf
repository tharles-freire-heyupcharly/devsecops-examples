# ISO 27018 - Auditoria e Rastreabilidade de Acesso a Dados Pessoais
# Objetivo: Registrar todos os acessos a dados pessoais para auditoria (LGPD Art. 37)

resource "aws_cloudtrail" "auditoria_dados_pessoais" {
  name                          = "cloudtrail-auditoria-dados-pessoais"
  s3_bucket_name                = aws_s3_bucket.logs_auditoria.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true

    data_resource {
      type   = "AWS::S3::Object"
      values = ["arn:aws:s3:::empresa-dados-pessoais-brasil/*"]
    }

    data_resource {
      type   = "AWS::DynamoDB::Table"
      values = ["arn:aws:dynamodb:*:*:table/usuarios-dados-pessoais"]
    }
  }

  tags = {
    Compliance = "ISO-27018"
    Control    = "Auditoria"
    LGPD       = "Art37"
  }
}

resource "aws_s3_bucket" "logs_auditoria" {
  bucket = "empresa-logs-auditoria-iso27018"

  tags = {
    Compliance = "ISO-27018"
    Purpose    = "AuditLogs"
  }
}

resource "aws_s3_bucket_versioning" "logs_versioning" {
  bucket = aws_s3_bucket.logs_auditoria.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "retencao_logs" {
  bucket = aws_s3_bucket.logs_auditoria.id

  rule {
    id     = "retencao-logs-7anos"
    status = "Enabled"

    expiration {
      days = 2555  # 7 anos - LGPD Art. 37
    }

    noncurrent_version_expiration {
      noncurrent_days = 365
    }
  }
}

resource "aws_cloudwatch_log_metric_filter" "acesso_suspeito" {
  name           = "acesso-dados-pessoais-fora-horario"
  log_group_name = "/aws/cloudtrail/auditoria-dados-pessoais"
  pattern        = "[time, request_id, event_type = GetObject || PutObject, user, ip]"

  metric_transformation {
    name      = "AcessoForaHorario"
    namespace = "ISO27018/Auditoria"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "alerta_acesso_anomalo" {
  alarm_name          = "iso27018-acesso-anomalo-dados-pessoais"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "AcessoForaHorario"
  namespace           = "ISO27018/Auditoria"
  period              = "300"
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "Detecta acessos anômalos a dados pessoais"
  treat_missing_data  = "notBreaching"

  tags = {
    Compliance = "ISO-27018"
    LGPD       = "MonitoramentoAcesso"
  }
}
