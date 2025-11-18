# 📊 Métricas e KPIs de Compliance Contínuo

## 🎯 Objetivos de Medição

Este documento define as métricas-chave para avaliar a efetividade da pipeline de compliance contínuo.

## 📈 KPIs Principais

### 1. Taxa de Conformidade
**Definição**: Percentual de execuções da pipeline que passaram em todas as validações.

```
Taxa de Conformidade = (Execuções Bem-sucedidas / Total de Execuções) × 100
```

**Meta**: ≥ 95%

**Medição**:
- ✅ Verde: ≥ 95%
- ⚠️ Amarelo: 90-94%
- ❌ Vermelho: < 90%

---

### 2. Tempo Médio de Execução (Lead Time)
**Definição**: Tempo total da pipeline do início ao deploy.

**Meta**: ≤ 15 minutos

**Breakdown por Stage**:
| Stage | SLA | Peso |
|-------|-----|------|
| Validação de Código | 1 min | 7% |
| Análise de Segurança | 2 min | 13% |
| Validação de Políticas | 5 min | 33% |
| Terraform Plan | 2 min | 13% |
| Relatório de Compliance | 1 min | 7% |
| Deploy (Production) | 5 min | 33% |
| Notificações | 1 min | 7% |

---

### 3. Mean Time to Detection (MTTD)
**Definição**: Tempo médio para detectar uma violação de compliance.

**Meta**: ≤ 5 minutos (desde o commit)

**Medição**:
```
MTTD = Tempo do Commit → Tempo da Detecção da Violação
```

---

### 4. Mean Time to Remediation (MTTR)
**Definição**: Tempo médio para corrigir uma violação de compliance.

**Meta**: ≤ 4 horas

**Medição**:
```
MTTR = Tempo da Detecção → Tempo do Fix em Produção
```

---

### 5. Violações por Categoria

**Categorias ISO 27017**:
- 🔴 Backup e Recuperação
- 🟠 Criptografia
- 🟡 Segregação de Rede

**Categorias ISO 27018**:
- 🔵 Auditoria
- 🟢 Direito ao Esquecimento
- 🟣 Data Residency

**Meta**: 0 violações críticas em produção

---

### 6. Cobertura de Políticas
**Definição**: Percentual de recursos cloud cobertos por políticas OPA.

```
Cobertura = (Recursos com Políticas / Total de Recursos) × 100
```

**Meta**: 100%

**Recursos Monitorados**:
- ✅ S3 Buckets
- ✅ RDS Databases
- ✅ EC2 Instances
- ✅ VPCs e Subnets
- ✅ KMS Keys
- ✅ CloudTrail Trails
- ✅ Lambda Functions
- ✅ DynamoDB Tables

---

### 7. Frequência de Execução
**Definição**: Número de execuções da pipeline por período.

**Meta**: 
- Mínimo: 1x/dia (scheduled)
- Real: ~10-20x/dia (PRs + commits)

**Breakdown**:
- 📅 Scheduled: ~30/mês
- 🔀 Pull Requests: ~40/mês
- 📤 Pushes to main: ~20/mês
- 👆 Manual: ~5/mês

**Total esperado**: ~95 execuções/mês

---

## 📊 Dashboard de Compliance

### Visualizações Recomendadas

#### 1. Gráfico de Tendência de Conformidade
```
100% ┤                    ╭────╮
 95% ┤          ╭────╮    │    │
 90% ┤    ╭─────╯    ╰────╯    │
 85% ┤────╯                    │
     └─────────────────────────┴─
      Jan  Feb  Mar  Apr  May
```

#### 2. Heatmap de Violações
```
          Backup  Crypto  Network  Audit  Erasure  Residency
Week 1:     0       0       1       0       0         0
Week 2:     0       0       0       0       1         0
Week 3:     0       1       0       0       0         0
Week 4:     0       0       0       0       0         0
```

#### 3. Funil de Execução
```
Total de Execuções: 100
│
├─ Validação OK: 98 (98%)
│  │
│  ├─ Segurança OK: 95 (97%)
│  │  │
│  │  ├─ Políticas OK: 92 (97%)
│  │  │  │
│  │  │  ├─ Plan OK: 90 (98%)
│  │  │  │  │
│  │  │  │  └─ Deploy: 85 (94%)
```

#### 4. Tempo de Execução por Stage
```
Validação     ████ 1 min
Segurança     ████████ 2 min
Políticas     ████████████████████ 5 min
Plan          ████████ 2 min
Relatório     ████ 1 min
Deploy        ████████████████████ 5 min
Notificações  ████ 1 min
```

---

## 🔔 Alertas e Thresholds

### Alertas Críticos (P1)
- ❌ Taxa de conformidade < 90%
- ❌ Violação de política ISO 27018 (LGPD)
- ❌ Deploy failed em produção
- ❌ MTTR > 24 horas

**Ação**: Notificação imediata para DPO + CTO

### Alertas Altos (P2)
- ⚠️ Taxa de conformidade 90-94%
- ⚠️ Violação de política ISO 27017
- ⚠️ Tempo de execução > 20 minutos
- ⚠️ MTTR > 8 horas

**Ação**: Notificação para Security Team + DevOps

### Alertas Médios (P3)
- 🟡 Taxa de conformidade 95-97%
- 🟡 MTTD > 10 minutos
- 🟡 Frequência de execução < 1/dia

**Ação**: Notificação para DevOps Lead

---

## 📋 Relatórios Periódicos

### Diário (Automático)
- ✅ Status da pipeline do dia anterior
- ✅ Violações detectadas e corrigidas
- ✅ Tempo médio de execução

**Destinatários**: DevOps Team, Security Team

### Semanal (Automático)
- ✅ Resumo de conformidade da semana
- ✅ Top 5 violações mais frequentes
- ✅ Tendências de melhoria/piora
- ✅ MTTR e MTTD médios

**Destinatários**: Security Lead, DevOps Lead, Compliance Team

### Mensal (Manual + Automático)
- ✅ Relatório executivo de compliance
- ✅ Análise de tendências (3 meses)
- ✅ Recomendações de melhorias
- ✅ ROI do compliance contínuo
- ✅ Comparação com benchmarks

**Destinatários**: CTO, CISO, DPO, Auditoria

### Trimestral (Manual)
- ✅ Auditoria completa de políticas
- ✅ Revisão de SLAs e métricas
- ✅ Apresentação ao Board
- ✅ Certificação ISO (se aplicável)

**Destinatários**: C-Level, Board, Auditores Externos

---

## 💰 ROI de Compliance Contínuo

### Custos Evitados

#### Multas LGPD/ISO
```
Multa média LGPD: R$ 10.000.000
Probabilidade sem compliance: 30%
Custo esperado: R$ 3.000.000

Com compliance contínuo:
Probabilidade: 5%
Custo esperado: R$ 500.000

Economia anual: R$ 2.500.000
```

#### Incidentes de Segurança
```
Incidentes/ano sem compliance: 12
Custo médio/incidente: R$ 200.000
Custo total: R$ 2.400.000

Com compliance contínuo:
Incidentes/ano: 2
Custo total: R$ 400.000

Economia anual: R$ 2.000.000
```

#### Tempo de Equipe
```
Auditorias manuais: 160h/mês × R$ 200/h = R$ 32.000/mês
Compliance contínuo: 20h/mês × R$ 200/h = R$ 4.000/mês

Economia mensal: R$ 28.000
Economia anual: R$ 336.000
```

### ROI Total Estimado
```
Economia Total: R$ 4.836.000/ano
Custo da Pipeline: R$ 50.000/ano (infra + manutenção)

ROI = (4.836.000 - 50.000) / 50.000 = 95,72x
```

**Payback**: < 1 semana

---

## 📊 Exemplo de Query (GitHub API)

```python
import requests
from datetime import datetime, timedelta

def get_pipeline_metrics(repo, days=30):
    """Busca métricas da pipeline via GitHub API"""
    
    url = f"https://api.github.com/repos/{repo}/actions/workflows/compliance-pipeline.yml/runs"
    params = {
        "created": f">={(datetime.now() - timedelta(days=days)).isoformat()}"
    }
    
    response = requests.get(url, params=params, headers={
        "Authorization": f"token {GITHUB_TOKEN}"
    })
    
    runs = response.json()["workflow_runs"]
    
    total = len(runs)
    success = sum(1 for r in runs if r["conclusion"] == "success")
    failed = sum(1 for r in runs if r["conclusion"] == "failure")
    
    avg_duration = sum(
        (datetime.fromisoformat(r["updated_at"]) - 
         datetime.fromisoformat(r["created_at"])).total_seconds()
        for r in runs
    ) / total
    
    return {
        "total_runs": total,
        "success_rate": (success / total) * 100,
        "failure_rate": (failed / total) * 100,
        "avg_duration_minutes": avg_duration / 60
    }

# Exemplo de uso
metrics = get_pipeline_metrics("empresa/infra-terraform", days=30)
print(f"Taxa de Conformidade: {metrics['success_rate']:.2f}%")
print(f"Tempo Médio: {metrics['avg_duration_minutes']:.1f} min")
```

---

**Última atualização**: 2025-11-18  
**Responsável**: Compliance Team  
**Revisão**: Trimestral
