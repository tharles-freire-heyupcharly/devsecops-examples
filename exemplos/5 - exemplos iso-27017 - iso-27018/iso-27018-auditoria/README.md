# ISO 27018 - Auditoria e Rastreabilidade de Acesso a Dados Pessoais

## 📋 Conceito

Este controle implementa **auditoria completa de acessos a dados pessoais**, atendendo LGPD Art. 37 (relatório de impacto à proteção de dados) e ISO 27018.

### Requisitos do Controle:
- ✅ CloudTrail capturando todos os acessos a dados pessoais
- ✅ Multi-região para auditoria global
- ✅ Validação de integridade dos logs (hash)
- ✅ Retenção de 7 anos (LGPD Art. 37)
- ✅ Detecção de anomalias em tempo real

## 💻 Código (main.tf)

O Terraform provisiona:
1. **CloudTrail** - Auditoria de eventos S3 e DynamoDB
2. **S3 Bucket para Logs** - Armazenamento imutável (versionamento)
3. **Lifecycle Policy** - Retenção de 7 anos
4. **CloudWatch Metric Filter** - Detecta acessos fora de horário
5. **CloudWatch Alarm** - Alerta sobre acessos anômalos

## 🔒 Validação OPA (policy.rego)

A política verifica:
- ✅ CloudTrail tem validação de logs habilitada (integridade)
- ✅ Trail é multi-região (auditoria completa)
- ✅ Data Events estão capturados (acesso a objetos S3/DynamoDB)
- ✅ Logs têm retenção >= 7 anos (LGPD)
- ✅ Bucket de auditoria tem versionamento
- ✅ Detecção de anomalias configurada

## 🎯 Impacto

### Benefícios de Compliance:
- **LGPD Art. 37**: Relatório de impacto disponível instantaneamente
- **Não-repúdio**: Prova inequívoca de quem acessou o que e quando
- **Investigação de incidentes**: Timeline completa de acessos
- **Conformidade**: ISO 27018, SOC 2, HIPAA, PCI DSS

### Métricas:
- **Eventos capturados**: ~1 milhão/dia (empresa média)
- **Latência de detecção**: < 5 minutos
- **Custo**: $2.00/100.000 eventos (CloudTrail)
- **Retenção**: 7 anos = 2.555 dias de logs

### Exemplo Real:
```
Antes: Sem auditoria → Vazamento descoberto após 6 meses
Depois: CloudTrail + alarmes → Acesso anômalo detectado em 2 minutos
```

## 📊 Demonstração

Execute o código:
```bash
terraform init
terraform plan
terraform apply
```

Consulte logs de auditoria:
```bash
# Liste eventos de acesso a S3
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceType,AttributeValue=AWS::S3::Object \
  --max-results 50

# Eventos específicos de um bucket
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=empresa-dados-pessoais-brasil

# Baixe logs para análise forense
aws s3 sync s3://empresa-logs-auditoria-iso27018/AWSLogs/ ./audit-logs/

# Verifique alarmes de anomalia
aws cloudwatch describe-alarms \
  --alarm-names iso27018-acesso-anomalo-dados-pessoais
```

Analise um acesso específico:
```bash
# Quem acessou arquivo X em data Y?
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=arn:aws:s3:::bucket/arquivo.csv \
  --start-time 2024-01-15T00:00:00Z \
  --end-time 2024-01-15T23:59:59Z
```

Valide com OPA:
```bash
terraform plan -out=plan.binary
terraform show -json plan.binary > plan.json
opa eval -i plan.json -d policy.rego "data.terraform.audit_compliance.deny"
```

## 🏢 Caso de Uso MBA

**Empresa**: Hospital com 500.000 prontuários eletrônicos (dados sensíveis LGPD)  
**Problema**: Paciente alegou que médico não autorizado acessou seu prontuário  
**Solução**: CloudTrail forneceu timeline completa de acessos com IP, horário e usuário  
**Resultado**:
- Processo judicial ganho em 1ª instância (prova irrefutável)
- Médico infrator identificado e desligado em 24h
- Conformidade LGPD + HIPAA mantida
- Economia de R$ 2 milhões em indenização potencial
- ANS (Agência Nacional de Saúde) aprovou certificação de segurança
