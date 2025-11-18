# 🔧 Troubleshooting - Pipeline de Compliance Contínuo

## 🚨 Problemas Comuns e Soluções

### 1. Pipeline falhou no Stage 1 (Validação de Código)

#### ❌ Erro: "Terraform format check failed"

**Causa**: Arquivos `.tf` não estão formatados corretamente.

**Solução**:
```bash
# Formatar todos os arquivos recursivamente
terraform fmt -recursive

# Verificar formatação
terraform fmt -check -recursive
```

#### ❌ Erro: "Terraform validation failed"

**Causa**: Sintaxe inválida em arquivos Terraform.

**Solução**:
```bash
# Validar sintaxe
cd <diretório-com-erro>
terraform init -backend=false
terraform validate

# Ver detalhes do erro
terraform validate -json | jq
```

---

### 2. Pipeline falhou no Stage 2 (Análise de Segurança)

#### ❌ Erro: "TFSec found HIGH severity issues"

**Causa**: Vulnerabilidades de segurança detectadas.

**Solução**:
```bash
# Executar TFSec localmente para ver detalhes
tfsec . --format=default

# Ver apenas problemas HIGH e CRITICAL
tfsec . --minimum-severity HIGH

# Gerar relatório HTML
tfsec . --format=html > tfsec-report.html
```

**Vulnerabilidades comuns**:
- 🔐 S3 bucket sem criptografia → Adicione `server_side_encryption_configuration`
- 🔓 Bucket público → Habilite `aws_s3_bucket_public_access_block`
- 🔑 KMS sem rotação → Configure `enable_key_rotation = true`

#### ❌ Erro: "Checkov found policy violations"

**Causa**: Violação de best practices CIS AWS Foundations.

**Solução**:
```bash
# Executar Checkov localmente
checkov -d . --framework terraform

# Ver apenas falhas críticas
checkov -d . --compact --quiet

# Suprimir checks específicos (com justificativa)
# Adicione no arquivo .tf:
# checkov:skip=CKV_AWS_123:Razão válida para exceção
```

---

### 3. Pipeline falhou no Stage 3 (Validação de Políticas)

#### ❌ Erro: "OPA policy denied"

**Causa**: Terraform plan viola política de compliance.

**Solução**:
```bash
# Testar política localmente
cd <diretório-da-política>

# Gerar plano
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json

# Testar política
opa eval -i tfplan.json -d policy.rego "data.terraform.deny"

# Ver detalhes da violação
opa eval -i tfplan.json -d policy.rego "data.terraform.deny" --format pretty
```

**Violações comuns**:

**ISO 27017 - Backup**:
```rego
# Violação: Retenção < 30 dias
# Solução: Altere em main.tf
lifecycle {
  delete_after = 30  # Mínimo 30 dias
}
```

**ISO 27017 - Criptografia**:
```rego
# Violação: Criptografia não é aws:kms
# Solução: Altere em main.tf
server_side_encryption_configuration {
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"  # Não use "AES256"
      kms_master_key_id = aws_kms_key.key.arn
    }
  }
}
```

**ISO 27018 - Auditoria**:
```rego
# Violação: Retenção de logs < 7 anos
# Solução: Altere em main.tf
retention_in_days = 2555  # 7 anos = 2555 dias
```

---

### 4. Pipeline falhou no Stage 4 (Terraform Plan)

#### ❌ Erro: "Error acquiring state lock"

**Causa**: Outro processo está executando Terraform no mesmo estado.

**Solução**:
```bash
# Verificar quem está com o lock
terraform force-unlock <LOCK_ID>

# ⚠️ Use com cuidado! Apenas se tiver certeza que nenhum outro processo está rodando
```

#### ❌ Erro: "Error loading state"

**Causa**: Bucket S3 de backend não existe ou sem permissões.

**Solução**:
```bash
# Verificar backend configuration
cat backend.tf

# Verificar se bucket existe
aws s3 ls s3://nome-do-bucket

# Verificar permissões IAM
aws sts get-caller-identity
```

---

### 5. Pipeline falhou no Stage 6 (Deploy)

#### ❌ Erro: "Terraform apply failed"

**Causa**: Erro durante aplicação das mudanças.

**Solução**:
```bash
# Ver logs completos da execução
# No GitHub Actions, baixe os logs da run

# Executar apply localmente para debug
terraform apply tfplan

# Se necessário, fazer rollback
terraform plan -destroy
terraform apply -destroy
```

#### ❌ Erro: "Environment approval required"

**Causa**: Deploy em produção requer aprovação manual.

**Solução**:
1. Vá em: Actions → Workflow run → Review deployments
2. Selecione `production`
3. Clique em `Approve and deploy`

---

### 6. Problemas com Secrets

#### ❌ Erro: "Secret not found"

**Causa**: Secret não configurado no GitHub.

**Solução**:
```bash
# Verificar secrets configurados
# Settings → Secrets and variables → Actions

# Adicionar secret
gh secret set AWS_ACCESS_KEY_ID --body "AKIAIOSFODNN7EXAMPLE"
gh secret set AWS_SECRET_ACCESS_KEY --body "wJalrXUtnFEMI/..."
```

#### ❌ Erro: "Invalid AWS credentials"

**Causa**: Credenciais AWS inválidas ou expiradas.

**Solução**:
```bash
# Testar credenciais localmente
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
aws sts get-caller-identity

# Gerar novas credenciais no IAM Console
# Atualizar secrets no GitHub
```

---

### 7. Problemas de Performance

#### ⚠️ Pipeline muito lenta (> 20 minutos)

**Causas e Soluções**:

1. **Muitos recursos para validar**
   ```yaml
   # Paralelizar validações
   strategy:
     matrix:
       policy: [backup, crypto, network, audit, erasure, residency]
   ```

2. **Terraform init lento**
   ```yaml
   # Cachear providers
   - uses: actions/cache@v3
     with:
       path: .terraform
       key: terraform-${{ hashFiles('.terraform.lock.hcl') }}
   ```

3. **OPA eval lento**
   ```bash
   # Usar opa test ao invés de eval
   opa test policy.rego
   ```

---

### 8. Problemas com Notificações

#### ❌ Slack não recebe notificações

**Solução**:
```bash
# Verificar webhook URL
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  $SLACK_WEBHOOK_URL

# Verificar secret configurado
gh secret list | grep SLACK
```

#### ❌ Email não chega

**Solução**:
```yaml
# Adicionar step de envio de email
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Pipeline Failed
    to: dpo@empresa.com
    from: github-actions@empresa.com
```

---

## 🔍 Debugging Avançado

### Habilitar Debug Logs

```yaml
# Adicione no workflow
env:
  TF_LOG: DEBUG
  OPA_LOG_LEVEL: debug
  ACTIONS_STEP_DEBUG: true
```

### Executar Step Específico Localmente

```bash
# Simular ambiente do GitHub Actions
docker run -it --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  hashicorp/terraform:1.6.0 \
  sh -c "terraform init && terraform validate"
```

### Validar Workflow YAML

```bash
# Instalar actionlint
brew install actionlint

# Validar workflow
actionlint .github/workflows/compliance-pipeline.yml
```

---

## 📞 Suporte

### Níveis de Suporte

**P1 - Crítico** (SLA: 1 hora)
- Pipeline bloqueando deploy de hotfix
- Violação de LGPD em produção
- Credenciais AWS comprometidas

**P2 - Alto** (SLA: 4 horas)
- Pipeline falhando em todos os PRs
- Políticas OPA com falsos positivos
- Performance muito degradada

**P3 - Médio** (SLA: 1 dia)
- Notificações não funcionando
- Documentação desatualizada
- Melhorias de usabilidade

**P4 - Baixo** (SLA: 1 semana)
- Dúvidas gerais
- Solicitação de novas features
- Otimizações

### Canais de Suporte

- 🔴 **P1**: Slack #incident-response + Pagerduty
- 🟠 **P2**: Slack #devops-support
- 🟡 **P3**: GitHub Issues
- 🟢 **P4**: GitHub Discussions

### Informações para Suporte

Ao abrir um ticket, inclua:
```
1. Workflow Run URL
2. Commit SHA
3. Branch
4. Logs completos (baixar artifact)
5. Passos para reproduzir
6. Impacto ao negócio
```

---

## 📚 Recursos Adicionais

- [Terraform Troubleshooting](https://www.terraform.io/docs/cli/commands/troubleshooting.html)
- [OPA Debugging](https://www.openpolicyagent.org/docs/latest/debugging/)
- [GitHub Actions Troubleshooting](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows)
- [TFSec Rules](https://aquasecurity.github.io/tfsec/)
- [Checkov Policies](https://www.checkov.io/5.Policy%20Index/all.html)

---

**Última atualização**: 2025-11-18  
**Mantenedor**: DevOps Team  
**Revisão**: Mensal
