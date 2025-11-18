# ISO 27017 - Controle de Backup e Recuperação em Nuvem
# Objetivo: Garantir backup automatizado e recuperação de dados críticos

resource "aws_backup_vault" "vault_conformidade" {
  name = "backup-vault-iso27017"

  tags = {
    Compliance = "ISO-27017"
    Control    = "Backup"
  }
}

resource "aws_backup_plan" "plano_diario" {
  name = "plano-backup-diario-iso27017"

  rule {
    rule_name         = "backup-diario-retencao-30d"
    target_vault_name = aws_backup_vault.vault_conformidade.name
    schedule          = "cron(0 3 * * ? *)" # 3AM UTC diariamente

    lifecycle {
      delete_after = 30
    }

    recovery_point_tags = {
      Compliance = "ISO-27017"
      Type       = "Automated"
    }
  }

  tags = {
    Compliance = "ISO-27017"
    Control    = "Backup"
  }
}

resource "aws_backup_selection" "selecao_recursos" {
  name         = "selecao-backup-producao"
  plan_id      = aws_backup_plan.plano_diario.id
  iam_role_arn = "arn:aws:iam::ACCOUNT_ID:role/service-role/AWSBackupDefaultServiceRole"

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Environment"
    value = "production"
  }

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "BackupRequired"
    value = "true"
  }
}

resource "aws_backup_vault_notifications" "notificacoes" {
  backup_vault_name   = aws_backup_vault.vault_conformidade.name
  sns_topic_arn       = "arn:aws:sns:us-east-1:ACCOUNT_ID:backup-notifications"
  backup_vault_events = ["BACKUP_JOB_FAILED", "RESTORE_JOB_COMPLETED"]
}
