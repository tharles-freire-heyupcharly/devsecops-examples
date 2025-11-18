# 🔒 Pipeline de Compliance Contínuo - ISO 27017/27018

## 📋 Visão Geral

Esta pipeline implementa **Compliance Contínuo** para infraestrutura cloud, validando automaticamente conformidade com:
- ✅ **ISO 27017** - Cloud Computing Security Controls
- ✅ **ISO 27018** - Personal Data Protection in Cloud
- ✅ **LGPD** - Lei Geral de Proteção de Dados (Brasil)

## 🏗️ Arquitetura da Pipeline

A pipeline é composta por **7 stages sequenciais**:

### STAGE 1: 📝 Validação de Código
- Verifica formatação do Terraform (`terraform fmt`)
- Valida sintaxe de todos os arquivos `.tf`
- **SLA**: ~1 minuto

### STAGE 2: 🛡️ Análise de Segurança (SAST)
- **TFSec**: Detecta vulnerabilidades em código Terraform
- **Checkov**: Valida best practices de segurança
- Upload de resultados SARIF para GitHub Security
- **SLA**: ~2 minutos

### STAGE 3: ⚖️ Validação de Políticas (OPA)
Valida 6 políticas de compliance:

#### ISO 27017:
1. **Backup e Recuperação** - Retenção mínima 30 dias
2. **Criptografia** - AES-256 com rotação automática
3. **Segregação de Rede** - VPCs isoladas Dev/Prod

#### ISO 27018:
4. **Auditoria** - CloudTrail multi-region, retenção 7 anos
5. **Direito ao Esquecimento** - SLA < 15 dias (LGPD)
6. **Data Residency** - Dados 100% em território brasileiro

**SLA**: ~5 minutos

### STAGE 4: 📋 Terraform Plan
- Gera plano de execução
- Comenta resultados em Pull Requests
- Salva artefato `tfplan` para deploy
- **SLA**: ~2 minutos

### STAGE 5: 📊 Relatório de Compliance
- Gera relatório consolidado em Markdown
- Calcula métricas de conformidade
- Upload de artefatos
- **SLA**: ~1 minuto

### STAGE 6: 🚀 Deploy (Production)
- **Executa apenas em `main` branch**
- Requer aprovação de ambiente
- Aplica mudanças com `terraform apply`
- Verifica conformidade pós-deploy
- **SLA**: ~5 minutos

### STAGE 7: 📧 Notificações
- Slack: Status da pipeline
- Email: DPO e Compliance Team
- **SLA**: ~1 minuto

## 🎯 Triggers

A pipeline executa automaticamente em:

```yaml
✅ Push para main ou develop
✅ Pull Requests para main
✅ Agendamento (cron): Diário às 3AM UTC
✅ Execução Manual (workflow_dispatch)
```

## 🚦 Gates de Qualidade

Cada stage possui um **gate** que bloqueia o fluxo se falhar:

```
Stage 1 (Validação) → ✅ PASS → Stage 2
                    → ❌ FAIL → Pipeline Failed ❌
```

**Política de Falha**: Qualquer violação = rollback completo

## 📦 Artefatos Gerados

| Artefato | Descrição |
|----------|-----------|
| `validation-report` | Resultados de validação de código |
| `security-sarif` | Resultados de TFSec + Checkov |
| `policy-report` | Resultados de validação OPA |
| `tfplan` | Plano de execução Terraform |
| `compliance-report` | Relatório consolidado de conformidade |

## 🔧 Configuração

### 1. Secrets do GitHub

Configure os seguintes secrets no repositório:

```bash
AWS_ACCESS_KEY_ID        # Credencial AWS
AWS_SECRET_ACCESS_KEY    # Credencial AWS
SLACK_WEBHOOK_URL        # Webhook Slack (opcional)
```

### 2. Estrutura de Diretórios

```
.github/workflows/
  └── compliance-pipeline.yml

exemplos/
  └── 5 - exemplos iso-27017 - iso-27018/
      ├── iso-27017-backup/
      │   ├── main.tf
      │   └── policy.rego
      ├── iso-27017-criptografia/
      ├── iso-27017-segregacao/
      ├── iso-27018-auditoria/
      ├── iso-27018-esquecimento/
      └── iso-27018-localizacao/
```

### 3. Ambiente de Produção

Configure um ambiente `production` no GitHub com:
- Aprovadores obrigatórios
- Wait timer (opcional)
- Protection rules

## 📊 Métricas de SLA

| Stage | Tempo Médio |
|-------|-------------|
| Validação de Código | ~1 min |
| Análise de Segurança | ~2 min |
| Validação de Políticas | ~5 min |
| Terraform Plan | ~2 min |
| Relatório de Compliance | ~1 min |
| Deploy (Production) | ~5 min |
| Notificações | ~1 min |
| **TOTAL** | **~17 min** |

## 🎨 Diagrama da Pipeline

Execute o script Python para gerar o diagrama visual:

```bash
python diagram.py
```

Isso gerará:
- `compliance-pipeline-architecture.png` (600 DPI)
- `compliance-pipeline-architecture.pdf` (vetorial)

## 🔒 Controles de Segurança Implementados

### Shift-Left Security
- Validação ocorre **antes** do deploy
- Feedback imediato em Pull Requests
- Bloqueia merge se houver violações

### Policy as Code (OPA)
- Regras de compliance em código
- Versionadas com a infraestrutura
- Testáveis e auditáveis

### Infrastructure as Code (Terraform)
- Estado versionado
- Mudanças rastreáveis
- Rollback facilitado

### Security as Code
- TFSec: Vulnerabilidades conhecidas
- Checkov: Best practices CIS AWS Foundations

## 📈 Nível de Conformidade

A pipeline garante:
- ✅ **100% de conformidade** antes do deploy
- ✅ **Zero tolerância** para violações críticas
- ✅ **Auditoria completa** de todas as mudanças
- ✅ **Rastreabilidade** de quem aprovou o que

## 🚀 Como Usar

### 1. Criar Pull Request

```bash
git checkout -b feature/nova-politica
# Faça suas mudanças
git add .
git commit -m "feat: adiciona política de backup"
git push origin feature/nova-politica
```

A pipeline executará automaticamente e comentará no PR.

### 2. Aprovar e Merge

Se todos os checks passarem (✅), faça merge para `main`.

### 3. Deploy Automático

Após merge em `main`, a pipeline:
1. Re-executa todas as validações
2. Solicita aprovação de ambiente
3. Aplica mudanças em produção
4. Notifica stakeholders

## 📧 Notificações

### Slack
Mensagem enviada ao canal configurado com:
- Status da pipeline (✅ SUCCESS / ❌ FAILED)
- Commit SHA
- Branch
- Link para execução

### Email
Email enviado ao DPO e Compliance Team em caso de:
- ❌ Falha de conformidade
- ✅ Deploy bem-sucedido em produção

## 🛠️ Troubleshooting

### Pipeline falhou no Stage 1
```bash
# Corrigir formatação
terraform fmt -recursive

# Validar sintaxe
terraform validate
```

### Pipeline falhou no Stage 2
```bash
# Executar TFSec localmente
tfsec .

# Executar Checkov localmente
checkov -d .
```

### Pipeline falhou no Stage 3
```bash
# Testar política OPA
opa test policy.rego

# Validar contra Terraform plan
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json
opa eval -i tfplan.json -d policy.rego "data.terraform.deny"
```

## 📚 Referências

- [ISO 27017:2015](https://www.iso.org/standard/43757.html) - Cloud Security Controls
- [ISO 27018:2019](https://www.iso.org/standard/76559.html) - Personal Data Protection
- [LGPD](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) - Lei 13.709/2018
- [Open Policy Agent](https://www.openpolicyagent.org/)
- [Terraform](https://www.terraform.io/)
- [TFSec](https://aquasecurity.github.io/tfsec/)
- [Checkov](https://www.checkov.io/)

## 📄 Licença

Este exemplo é fornecido para fins educacionais.

---

**Gerado por**: Pipeline de Compliance Contínuo  
**Última atualização**: 2025-11-18
