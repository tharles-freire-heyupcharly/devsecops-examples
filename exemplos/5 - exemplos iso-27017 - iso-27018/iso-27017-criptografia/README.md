# ISO 27017 - Controle de Criptografia em Nuvem

## 📋 Conceito

Este controle implementa **criptografia de dados em repouso** para proteger informações sensíveis armazenadas na nuvem, conforme requisitos da ISO 27017.

### Requisitos do Controle:
- ✅ Criptografia obrigatória para dados sensíveis
- ✅ Uso de chaves gerenciadas (AWS KMS)
- ✅ Rotação automática de chaves
- ✅ Bloqueio de acesso público
- ✅ Rastreabilidade através de tags de compliance

## 💻 Código (main.tf)

O Terraform provisiona:
1. **AWS KMS Key** - Chave mestra para criptografia
2. **S3 Bucket** - Armazenamento de dados conformes
3. **Server-Side Encryption** - Criptografia automática (AES-256)
4. **Public Access Block** - Previne exposição pública

## 🔒 Validação OPA (policy.rego)

A política Open Policy Agent verifica:
- ✅ Buckets S3 têm criptografia habilitada
- ✅ Algoritmo de criptografia é `aws:kms` (não AES256 padrão)
- ✅ Chaves KMS têm rotação automática ativa
- ✅ Relacionamento correto entre bucket e configuração de criptografia

## 🎯 Impacto

### Benefícios de Segurança:
- **Proteção contra vazamento**: Dados ilegíveis sem a chave KMS
- **Conformidade**: Atende LGPD, PCI DSS, HIPAA, SOC 2
- **Defesa em profundidade**: Criptografia + controles de acesso

### Métricas:
- **Nível de proteção**: AES-256 (padrão militar)
- **Rotação de chaves**: Automática a cada 365 dias
- **Impacto em performance**: < 5% overhead

### Exemplo Real:
```
Antes: Bucket exposto → Dados em texto claro
Depois: Bucket criptografado → Dados protegidos mesmo se acessados indevidamente
```

## 📊 Demonstração

Execute o código:
```bash
terraform init
terraform plan
terraform apply
```

Valide com OPA:
```bash
terraform plan -out=plan.binary
terraform show -json plan.binary > plan.json
opa eval -i plan.json -d policy.rego "data.terraform.s3_encryption.deny"
```

## 🏢 Caso de Uso MBA

**Empresa**: Fintech com dados de clientes (CPF, transações financeiras)  
**Problema**: Regulação do Banco Central exige criptografia de dados  
**Solução**: Implementação automatizada via IaC + validação contínua com OPA  
**Resultado**: Aprovação em auditoria PCI DSS sem intervenção manual
