# 📑 Índice - Pipeline de Compliance Contínuo

## 📁 Estrutura de Arquivos

```
6 - pipeline compliance continuo/
├── 📄 README.md                                    ⭐ Comece aqui!
├── 📊 METRICS.md                                   Métricas e KPIs
├── 🔧 TROUBLESHOOTING.md                           Guia de resolução de problemas
├── 📑 INDEX.md                                     Este arquivo
│
├── 🤖 .github/workflows/
│   └── compliance-pipeline.yml                     Pipeline GitHub Actions
│
├── 🐍 diagram.py                                   Gerador de diagrama
├── 🖼️  compliance-pipeline-architecture.png        Diagrama PNG (600 DPI)
├── 📄 compliance-pipeline-architecture.pdf         Diagrama PDF (vetorial)
│
├── 🔒 .env.example                                 Exemplo de configuração
├── 🚫 .gitignore                                   Arquivos ignorados pelo Git
├── 👥 CODEOWNERS                                   Donos de código
└── 🏃 run-local.sh                                 Script de execução local
```

## 🚀 Quick Start

### 1️⃣ Primeira Execução

```bash
# Clone o repositório
git clone <url-do-repo>
cd "6 - pipeline compliance continuo"

# Leia a documentação principal
cat README.md

# Configure secrets (veja .env.example)
cp .env.example .env
# Edite .env com suas credenciais

# Execute validação local
./run-local.sh
```

### 2️⃣ Gerar Diagrama

```bash
# Execute o script Python
python diagram.py

# Visualize o diagrama
open compliance-pipeline-architecture.png
open compliance-pipeline-architecture.pdf
```

### 3️⃣ Configurar GitHub Actions

```bash
# Copie o workflow para seu repositório
mkdir -p .github/workflows
cp .github/workflows/compliance-pipeline.yml .github/workflows/

# Configure secrets no GitHub
gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set SLACK_WEBHOOK_URL  # Opcional

# Faça commit e push
git add .github/workflows/compliance-pipeline.yml
git commit -m "feat: adiciona pipeline de compliance contínuo"
git push
```

## 📚 Guias de Leitura

### Para Desenvolvedores

1. **Primeiro uso**: [README.md](README.md)
2. **Execução local**: [run-local.sh](run-local.sh)
3. **Problemas?**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Para DevOps/SRE

1. **Configuração**: [.env.example](.env.example)
2. **Pipeline completa**: [compliance-pipeline.yml](.github/workflows/compliance-pipeline.yml)
3. **Métricas**: [METRICS.md](METRICS.md)
4. **Code Owners**: [CODEOWNERS](CODEOWNERS)

### Para Compliance/Auditoria

1. **Visão geral**: [README.md](README.md) → Seção "Controles de Segurança"
2. **Métricas e KPIs**: [METRICS.md](METRICS.md)
3. **Diagrama visual**: [compliance-pipeline-architecture.pdf](compliance-pipeline-architecture.pdf)

### Para Gestores/C-Level

1. **ROI**: [METRICS.md](METRICS.md) → Seção "ROI de Compliance Contínuo"
2. **Dashboards**: [METRICS.md](METRICS.md) → Seção "Dashboard de Compliance"
3. **Diagrama executivo**: [compliance-pipeline-architecture.pdf](compliance-pipeline-architecture.pdf)

## 🎯 Casos de Uso

### Criar novo Pull Request

```bash
# 1. Crie branch
git checkout -b feature/nova-politica

# 2. Faça mudanças
vim exemplos/5\ -\ exemplos\ iso-27017\ -\ iso-27018/iso-27017-backup/main.tf

# 3. Valide localmente
./run-local.sh

# 4. Commit e push
git add .
git commit -m "feat: aumenta retenção de backup para 60 dias"
git push origin feature/nova-politica

# 5. Crie PR no GitHub
# Pipeline executará automaticamente
```

### Debugar falha na pipeline

```bash
# 1. Veja os logs no GitHub Actions
# 2. Consulte TROUBLESHOOTING.md
cat TROUBLESHOOTING.md

# 3. Reproduza localmente
./run-local.sh

# 4. Corrija o problema
# 5. Teste novamente
```

### Adicionar nova política OPA

```bash
# 1. Crie diretório da política
mkdir "exemplos/5 - exemplos iso-27017 - iso-27018/nova-politica"

# 2. Crie arquivos
cd "exemplos/5 - exemplos iso-27017 - iso-27018/nova-politica"
touch main.tf policy.rego README.md

# 3. Implemente a política em policy.rego
# 4. Adicione stage na pipeline
vim .github/workflows/compliance-pipeline.yml

# 5. Teste localmente
opa test policy.rego

# 6. Commit e PR
```

## 📊 Visualizações

### Diagrama da Pipeline

![Pipeline Architecture](compliance-pipeline-architecture.png)

**Versões disponíveis**:
- 🖼️ PNG (600 DPI): `compliance-pipeline-architecture.png`
- 📄 PDF (vetorial): `compliance-pipeline-architecture.pdf`

### 7 Stages da Pipeline

```
Trigger → Validação → Segurança → Políticas → Plan → Report → Deploy → Notify
  ⏱️       1 min      2 min      5 min     2 min   1 min    5 min   1 min
  
Total: ~17 minutos
```

## 🔗 Links Úteis

### Documentação Externa

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Terraform Registry](https://registry.terraform.io/)
- [OPA Playground](https://play.openpolicyagent.org/)
- [ISO 27017](https://www.iso.org/standard/43757.html)
- [ISO 27018](https://www.iso.org/standard/76559.html)
- [LGPD](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)

### Ferramentas

- [TFSec](https://aquasecurity.github.io/tfsec/)
- [Checkov](https://www.checkov.io/)
- [Open Policy Agent](https://www.openpolicyagent.org/)
- [Terraform](https://www.terraform.io/)

## 🏷️ Tags de Versão

- **v1.0.0** - Versão inicial
  - ✅ Pipeline completa de 7 stages
  - ✅ Validação de 6 políticas ISO
  - ✅ Integração GitHub Actions
  - ✅ Documentação completa

## 🤝 Contribuindo

### Reportar Bug

1. Verifique se não é um problema conhecido em [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Abra issue no GitHub com template:
   ```
   **Descrição**: 
   **Passos para reproduzir**:
   **Comportamento esperado**:
   **Logs**:
   ```

### Sugerir Melhoria

1. Abra GitHub Discussion
2. Descreva a melhoria
3. Justifique o valor agregado

### Submeter Pull Request

1. Leia [CODEOWNERS](CODEOWNERS)
2. Execute `./run-local.sh` antes de commitar
3. Garanta que pipeline passa
4. Solicite review dos code owners

## 📞 Suporte

### Canais

- 🔴 **Urgente**: Slack #incident-response
- 🟠 **Alta prioridade**: Slack #devops-support  
- 🟡 **Média prioridade**: GitHub Issues
- 🟢 **Baixa prioridade**: GitHub Discussions

### SLA

- P1 (Crítico): 1 hora
- P2 (Alto): 4 horas
- P3 (Médio): 1 dia
- P4 (Baixo): 1 semana

## 📅 Manutenção

### Atualizações

- **Diária**: Execução automática da pipeline (3AM UTC)
- **Semanal**: Review de métricas
- **Mensal**: Atualização de documentação
- **Trimestral**: Auditoria completa de políticas

### Versões de Dependências

```yaml
Terraform: 1.6.0
OPA: 0.58.0
Python: 3.11
TFSec: latest
Checkov: latest
```

## 🎓 Recursos de Aprendizado

### Tutoriais

1. [Como criar sua primeira política OPA](https://www.openpolicyagent.org/docs/latest/policy-language/)
2. [Terraform Best Practices](https://www.terraform-best-practices.com/)
3. [GitHub Actions CI/CD](https://docs.github.com/en/actions/guides)

### Vídeos

1. [OPA Deep Dive](https://www.youtube.com/watch?v=Yup1FUc2Qn0)
2. [Terraform Security Best Practices](https://www.youtube.com/watch?v=IFhx8NXPdKE)
3. [Compliance as Code](https://www.youtube.com/watch?v=SDQ-bGqT3nw)

---

**Versão**: 1.0.0  
**Data**: 2025-11-18  
**Mantenedor**: DevOps Team  
**Licença**: Educational Use
