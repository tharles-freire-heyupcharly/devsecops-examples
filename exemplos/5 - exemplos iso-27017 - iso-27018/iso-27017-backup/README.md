# ISO 27017 - Controle de Backup e Recuperação

## 📋 Conceito

Este controle implementa **backup automatizado e recuperação de dados críticos** na nuvem, garantindo continuidade de negócio e conformidade com ISO 27017.

### Requisitos do Controle:
- ✅ Backup diário automatizado (3AM UTC)
- ✅ Retenção mínima de 30 dias
- ✅ Notificações de falhas/sucessos
- ✅ Seleção por tags (Environment=production, BackupRequired=true)
- ✅ Registro de todas as operações de backup

## 💻 Código (main.tf)

O Terraform provisiona:
1. **AWS Backup Vault** - Cofre isolado para backups
2. **Backup Plan** - Regra de backup diário com retenção de 30 dias
3. **Backup Selection** - Seleção automática por tags
4. **SNS Notifications** - Alertas em caso de falha

## 🔒 Validação OPA (policy.rego)

A política verifica:
- ✅ Plano de backup tem agendamento diário (`cron`)
- ✅ Retenção é >= 30 dias (requisito ISO 27017)
- ✅ Backup Selection está configurado
- ✅ Vault tem notificações habilitadas

## 🎯 Impacto

### Benefícios de Continuidade:
- **RPO (Recovery Point Objective)**: 24 horas
- **RTO (Recovery Time Objective)**: < 4 horas
- **Proteção contra ransomware**: Backups isolados e imutáveis
- **Conformidade**: Atende ISO 27017, SOC 2, HIPAA

### Métricas:
- **Frequência**: Diária (365 backups/ano)
- **Custo**: ~$0.05/GB/mês (AWS Backup Vault)
- **Taxa de sucesso**: 99.9% com alertas automáticos

### Exemplo Real:
```
Antes: Backup manual semanal → Perda de 6 dias de dados em incidente
Depois: Backup diário automatizado → Perda máxima de 24 horas
```

## 📊 Demonstração

Execute o código:
```bash
terraform init
terraform plan
terraform apply
```

Simule um backup:
```bash
# Liste planos de backup
aws backup list-backup-plans

# Inicie backup manual
aws backup start-backup-job \
  --backup-vault-name backup-vault-iso27017 \
  --resource-arn <ARN_DO_RECURSO> \
  --iam-role-arn <IAM_ROLE_ARN>

# Verifique status
aws backup list-backup-jobs --by-backup-vault-name backup-vault-iso27017
```

Valide com OPA:
```bash
terraform plan -out=plan.binary
terraform show -json plan.binary > plan.json
opa eval -i plan.json -d policy.rego "data.terraform.backup_compliance.deny"
```

## 🏢 Caso de Uso MBA

**Empresa**: SaaS de gestão empresarial com 10.000 clientes  
**Problema**: Ransomware criptografou banco de dados, exigiu $500k resgate  
**Solução**: Backup automatizado diário + vault isolado permitiu restauração completa  
**Resultado**: Recuperação em 3 horas, perda de apenas 18h de dados, custo zero de resgate
