# ISO 27018 - Controle de Localização de Dados (Data Residency)

## 📋 Conceito

Este controle garante que **dados pessoais permaneçam em região geográfica específica** (Brasil), atendendo requisitos da LGPD e ISO 27018 sobre soberania de dados.

### Requisitos do Controle:
- ✅ Dados armazenados exclusivamente em região brasileira
- ✅ Bloqueio de replicação cross-region
- ✅ Retenção de dados conforme LGPD (máximo 5 anos)
- ✅ Tags obrigatórias: Region, LGPD, DataType
- ✅ AWS Config monitorando localização

## 💻 Código (main.tf)

O Terraform provisiona:
1. **S3 Bucket** - Região `sa-east-1` (São Paulo)
2. **Bucket Policy** - Bloqueio de replicação para outras regiões
3. **Lifecycle Policy** - Expiração automática após 5 anos (LGPD)
4. **AWS Config Rule** - Monitoramento contínuo de localização

## 🔒 Validação OPA (policy.rego)

A política verifica:
- ✅ Buckets de dados pessoais têm tag `Region` e `LGPD`
- ✅ Replicação cross-region está desabilitada
- ✅ Retenção não excede 5 anos (LGPD Art. 15)
- ✅ Bucket classificado como `DataType: PersonalData`

## 🎯 Impacto

### Benefícios de Compliance:
- **Soberania de dados**: 100% dos dados permanecem no Brasil
- **LGPD**: Atende Art. 11 (transferência internacional de dados)
- **Transparência**: Titular sabe exatamente onde seus dados estão
- **Multas evitadas**: LGPD pode multar até 2% do faturamento

### Métricas:
- **Localização**: 100% em `sa-east-1` (São Paulo, Brasil)
- **Latência**: ~15ms para usuários no Brasil
- **Custo**: Sem custos de transferência entre regiões

### Exemplo Real:
```
Antes: Dados replicados globalmente → Violação LGPD Art. 33
Depois: Dados exclusivos no Brasil → Conformidade total LGPD
```

## 📊 Demonstração

Execute o código:
```bash
# IMPORTANTE: Configure AWS CLI para região Brasil
export AWS_DEFAULT_REGION=sa-east-1

terraform init
terraform plan
terraform apply
```

Verifique a localização:
```bash
# Confirme que bucket está em sa-east-1
aws s3api get-bucket-location --bucket empresa-dados-pessoais-brasil

# Verifique políticas de bloqueio
aws s3api get-bucket-policy --bucket empresa-dados-pessoais-brasil

# Monitore com Config
aws configservice describe-compliance-by-config-rule \
  --config-rule-names s3-dados-pessoais-regiao-brasil
```

Valide com OPA:
```bash
terraform plan -out=plan.binary
terraform show -json plan.binary > plan.json
opa eval -i plan.json -d policy.rego "data.terraform.data_residency.deny"
```

## 🏢 Caso de Uso MBA

**Empresa**: Banco digital com 5 milhões de clientes brasileiros  
**Problema**: ANPD (Autoridade Nacional de Proteção de Dados) abriu investigação sobre dados armazenados na Irlanda  
**Solução**: Migração de todos os dados para `sa-east-1` + bloqueio de replicação  
**Resultado**: Investigação arquivada, conformidade 100% LGPD, confiança do cliente aumentou 40%
