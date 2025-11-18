# ISO 27018 - Direito ao Esquecimento (Right to Erasure - LGPD Art. 18)
# Objetivo: Automatizar exclusão de dados pessoais mediante solicitação do titular

resource "aws_lambda_function" "processar_esquecimento" {
  filename      = "esquecimento_handler.zip"
  function_name = "lgpd-direito-esquecimento"
  role          = "arn:aws:iam::ACCOUNT_ID:role/lambda-esquecimento-role"
  handler       = "index.handler"
  runtime       = "python3.11"
  timeout       = 300

  environment {
    variables = {
      BUCKET_DADOS_PESSOAIS = "empresa-dados-pessoais-brasil"
      DYNAMODB_TABLE        = "usuarios-dados-pessoais"
      SQS_QUEUE_URL         = aws_sqs_queue.fila_esquecimento.url
    }
  }

  tags = {
    Compliance = "ISO-27018"
    Control    = "Esquecimento"
    LGPD       = "Art18-Inciso-VI"
  }
}

resource "aws_sqs_queue" "fila_esquecimento" {
  name                      = "lgpd-solicitacoes-esquecimento"
  delay_seconds             = 0
  max_message_size          = 262144
  message_retention_seconds = 1209600 # 14 dias
  receive_wait_time_seconds = 10

  tags = {
    Compliance = "ISO-27018"
    LGPD       = "RightToErasure"
  }
}

resource "aws_cloudwatch_log_group" "logs_esquecimento" {
  name              = "/aws/lambda/lgpd-direito-esquecimento"
  retention_in_days = 2555 # 7 anos - auditoria LGPD

  tags = {
    Compliance = "ISO-27018"
    Purpose    = "AuditoriaEsquecimento"
  }
}

resource "aws_dynamodb_table" "registro_exclusoes" {
  name         = "lgpd-registro-exclusoes"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "usuario_id"
  range_key    = "timestamp_solicitacao"

  attribute {
    name = "usuario_id"
    type = "S"
  }

  attribute {
    name = "timestamp_solicitacao"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Compliance = "ISO-27018"
    LGPD       = "RegistroExclusoes"
  }
}
