#!/usr/bin/env python3
"""
Gerador de Apresentação PowerPoint - DevSecOps Examples
Gera apresentação sobre ISO 27017/27018 e Pipeline de Compliance Contínuo
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os

def create_presentation():
    """Cria apresentação PowerPoint sobre as pastas 5 e 6"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Slide 1: Título
    add_title_slide(prs)
    
    # Slide 2: Visão Geral ISO 27017/27018
    add_iso_overview_slide(prs)
    
    # Slide 3: ISO 27017 - Backup
    add_iso27017_backup_slide(prs)
    
    # Slide 4: ISO 27017 - Criptografia
    add_iso27017_encryption_slide(prs)
    
    # Slide 5: ISO 27017 - Segregação
    add_iso27017_segregation_slide(prs)
    
    # Slide 6: ISO 27018 - Auditoria
    add_iso27018_audit_slide(prs)
    
    # Slide 7: ISO 27018 - Esquecimento
    add_iso27018_erasure_slide(prs)
    
    # Slide 8: ISO 27018 - Localização
    add_iso27018_location_slide(prs)
    
    # Slide 9: Pipeline - Visão Geral
    add_pipeline_overview_slide(prs)
    
    # Slide 10: Pipeline - Stages 1-3
    add_pipeline_stages_1_3_slide(prs)
    
    # Slide 11: Pipeline - Stages 4-5
    add_pipeline_stages_4_5_slide(prs)
    
    # Slide 12: Pipeline - Métricas
    add_pipeline_metrics_slide(prs)
    
    # Slide 13: Conclusão
    add_conclusion_slide(prs)
    
    # Salvar apresentação
    output_file = "DevSecOps_ISO27017_27018_Presentation.pptx"
    prs.save(output_file)
    print(f"✅ Apresentação criada: {output_file}")
    return output_file

def set_text_format(text_frame, font_size=20, font_name="Arial", bold=False):
    """Define formatação padrão do texto"""
    for paragraph in text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.name = font_name
            run.font.size = Pt(font_size)
            run.font.bold = bold

def add_title_slide(prs):
    """Slide 1: Título"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # Título principal
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.text = "DevSecOps & Compliance Contínuo"
    title_para = title_frame.paragraphs[0]
    title_para.alignment = PP_ALIGN.CENTER
    title_para.font.size = Pt(44)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(0, 51, 102)
    
    # Subtítulo
    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(3.8), Inches(8), Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "ISO 27017/27018 & Pipeline Automatizada"
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.alignment = PP_ALIGN.CENTER
    subtitle_para.font.size = Pt(28)
    subtitle_para.font.name = "Arial"
    subtitle_para.font.color.rgb = RGBColor(64, 64, 64)
    
    # Rodapé
    footer_box = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(8), Inches(0.5))
    footer_frame = footer_box.text_frame
    footer_frame.text = "Exemplos práticos de conformidade em Cloud Computing"
    footer_para = footer_frame.paragraphs[0]
    footer_para.alignment = PP_ALIGN.CENTER
    footer_para.font.size = Pt(16)
    footer_para.font.name = "Arial"
    footer_para.font.color.rgb = RGBColor(128, 128, 128)

def add_iso_overview_slide(prs):
    """Slide 2: Visão Geral ISO 27017/27018"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🔒 ISO 27017/27018 - Visão Geral"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(0, 51, 102)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """📋 ISO 27017 - Cloud Computing Security
• Controles de segurança específicos para cloud
• Backup e recuperação de dados
• Criptografia de dados em repouso e trânsito
• Segregação de ambientes (Dev/Prod)

📋 ISO 27018 - Personal Data Protection
• Proteção de dados pessoais na nuvem
• Auditoria e rastreabilidade (CloudTrail)
• Direito ao esquecimento (LGPD Art. 18)
• Data residency - localização dos dados

🎯 Objetivo: Conformidade automatizada via IaC"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(12)

def add_iso27017_backup_slide(prs):
    """Slide 3: ISO 27017 - Backup"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "💾 ISO 27017 - Backup e Recuperação"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(0, 102, 51)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """✅ Requisitos de Conformidade:
• Backup automatizado diário às 3AM UTC
• Retenção mínima de 30 dias
• Vault dedicado para compliance (aws_backup_vault)
• Tags de rastreabilidade (Compliance, Type)

🛠️ Implementação AWS:
• AWS Backup Plan com regras de lifecycle
• Seleção por tags (Environment=production)
• Notificações SNS para falhas
• IAM Role com permissões específicas

📊 Validação OPA:
• Política verifica retenção >= 30 dias
• Valida tags obrigatórias de compliance"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(10)

def add_iso27017_encryption_slide(prs):
    """Slide 4: ISO 27017 - Criptografia"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🔐 ISO 27017 - Criptografia"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(0, 102, 51)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """✅ Requisitos de Conformidade:
• Criptografia AES-256 para dados em repouso
• KMS com rotação automática de chaves (365 dias)
• Bucket versionamento habilitado
• Logging de acesso às chaves

🛠️ Implementação AWS:
• AWS KMS Customer Managed Key
• S3 bucket encryption (SSE-KMS)
• Versioning e lifecycle management
• CloudWatch Logs para auditoria

📊 Validação OPA:
• Verifica algoritmo AES-256
• Valida rotação automática de chaves
• Confirma versionamento habilitado"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(10)

def add_iso27017_segregation_slide(prs):
    """Slide 5: ISO 27017 - Segregação"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🏗️ ISO 27017 - Segregação de Rede"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(0, 102, 51)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """✅ Requisitos de Conformidade:
• VPCs separadas para Dev e Prod
• CIDR blocks não sobrepostos
• Subnets públicas e privadas isoladas
• Flow Logs habilitados para auditoria

🛠️ Implementação AWS:
• VPC Dev: 10.0.0.0/16
• VPC Prod: 10.1.0.0/16
• Subnets em múltiplas AZs
• VPC Flow Logs para CloudWatch

📊 Validação OPA:
• Verifica VPCs separadas Dev/Prod
• Valida CIDR blocks distintos
• Confirma Flow Logs habilitados"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(10)

def add_iso27018_audit_slide(prs):
    """Slide 6: ISO 27018 - Auditoria"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "📋 ISO 27018 - Auditoria e Rastreabilidade"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(102, 0, 153)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """✅ Requisitos de Conformidade:
• CloudTrail multi-region habilitado
• Retenção de logs por 7 anos (2557 dias)
• Logs imutáveis (Object Lock)
• Criptografia de logs (KMS)

🛠️ Implementação AWS:
• CloudTrail com bucket S3 dedicado
• S3 Object Lock em modo Compliance
• Lifecycle para arquivamento Glacier
• Notificações SNS para eventos críticos

📊 Validação OPA:
• Verifica multi-region habilitado
• Valida retenção >= 2555 dias
• Confirma Object Lock ativo"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(10)

def add_iso27018_erasure_slide(prs):
    """Slide 7: ISO 27018 - Direito ao Esquecimento"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🗑️ ISO 27018 - Direito ao Esquecimento"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(102, 0, 153)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """✅ Requisitos de Conformidade (LGPD Art. 18):
• Processamento em até 15 dias
• Lambda function automatizada
• Fila SQS com retenção de 14 dias
• Registro completo de exclusões (DynamoDB)

🛠️ Implementação AWS:
• Lambda Python 3.11 com timeout 300s
• SQS para gerenciar solicitações
• DynamoDB para histórico de exclusões
• CloudWatch Logs (retenção 7 anos)

📊 Validação OPA:
• Verifica SLA de processamento
• Valida retenção de logs
• Confirma registro de exclusões"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(10)

def add_iso27018_location_slide(prs):
    """Slide 8: ISO 27018 - Localização de Dados"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🌎 ISO 27018 - Data Residency (LGPD)"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(32)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(102, 0, 153)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """✅ Requisitos de Conformidade:
• Dados pessoais 100% em sa-east-1 (Brasil)
• Bloqueio de replicação cross-region
• Lifecycle com retenção 5 anos (LGPD)
• Config Rule para validação contínua

🛠️ Implementação AWS:
• S3 bucket na região sa-east-1
• Bucket policy bloqueando replicação
• Tags: Region=Brazil, LGPD=true
• AWS Config para monitoramento

📊 Validação OPA:
• Verifica tags de localização
• Confirma bloqueio de replicação
• Valida conformidade LGPD"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(10)

def add_pipeline_overview_slide(prs):
    """Slide 9: Pipeline - Visão Geral"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "🚀 Pipeline de Compliance Contínuo"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(204, 51, 0)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """🎯 Objetivo:
Validação automatizada de conformidade em cada commit

⚙️ Tecnologias:
• GitHub Actions (CI/CD)
• Terraform 1.6.0 (IaC)
• Open Policy Agent - OPA 0.58.0
• TFSec & Checkov (SAST)
• Infracost (Estimativa de custos)

📊 7 Stages Automatizados:
1. Validação de Código
2. Análise de Segurança (SAST)
3. Validação de Políticas (OPA)
4. Terraform Plan
5. Estimativa de Custos
6. Relatório de Compliance
7. Deploy (desabilitado - exemplos)"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(8)

def add_pipeline_stages_1_3_slide(prs):
    """Slide 10: Pipeline Stages 1-3"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "📝 Pipeline - Stages 1-3"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(204, 51, 0)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5.2))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """Stage 1 - Validação de Código:
• terraform fmt -check (formatação)
• terraform validate (sintaxe)
• SLA: ~1 minuto

Stage 2 - Análise de Segurança (SAST):
• TFSec: vulnerabilidades em Terraform
• Checkov: best practices de segurança
• Upload SARIF para GitHub Security
• SLA: ~2 minutos

Stage 3 - Validação de Políticas (OPA):
• 6 políticas ISO 27017/27018
• terraform plan + opa eval
• Validação com mock credentials
• SLA: ~5 minutos"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(8)

def add_pipeline_stages_4_5_slide(prs):
    """Slide 11: Pipeline Stages 4-5"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "📋 Pipeline - Stages 4-6"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(204, 51, 0)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5.2))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """Stage 4 - Terraform Plan:
• Plan com -refresh=false
• Mock AWS provider para exemplos
• Upload de artefatos
• SLA: ~2 minutos

Stage 5 - Estimativa de Custos (Infracost):
• Análise de todos os 6 exemplos
• Relatório de custos AWS
• Comentários automáticos em PRs
• SLA: ~2 minutos

Stage 6 - Relatório de Compliance:
• Consolidação de resultados
• Métricas de conformidade
• Upload de artefatos
• SLA: ~1 minuto"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(8)

def add_pipeline_metrics_slide(prs):
    """Slide 12: Pipeline Métricas"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "📈 Métricas e Benefícios"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(204, 51, 0)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """⏱️ Performance:
• Tempo total: ~13 minutos
• Execução paralela de stages
• Continue-on-error para visibilidade total

✅ Conformidade:
• 6 políticas validadas automaticamente
• 50+ checks de segurança (Checkov/TFSec)
• 100% rastreabilidade via artefatos

🎯 Automação:
• Execução em push, PR, schedule (diário 3AM)
• Workflow dispatch para execução manual
• Comentários automáticos em Pull Requests

💰 Economia:
• Mock credentials - sem custos AWS
• Validação antes do deploy
• Prevenção de não-conformidade"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(10)

def add_conclusion_slide(prs):
    """Slide 13: Conclusão"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Título
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "✅ Conclusão"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(36)
    title_para.font.bold = True
    title_para.font.name = "Arial"
    title_para.font.color.rgb = RGBColor(0, 102, 51)
    
    # Conteúdo
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    content = """🎯 Principais Conquistas:

✅ Compliance automatizado ISO 27017/27018
✅ Pipeline CI/CD completa com 6 stages
✅ Policy as Code com Open Policy Agent
✅ Segurança integrada (SAST + OPA)
✅ Estimativa de custos automatizada
✅ 100% rastreável e auditável

🚀 Próximos Passos:

• Integrar com ambiente real AWS
• Adicionar testes de integração
• Implementar deploy automatizado
• Expandir políticas OPA
• Dashboard de métricas

📚 Recursos: github.com/tharles-freire-heyupcharly/devsecops-examples"""
    
    content_frame.text = content
    for paragraph in content_frame.paragraphs:
        paragraph.font.size = Pt(20)
        paragraph.font.name = "Arial"
        paragraph.space_after = Pt(10)

if __name__ == "__main__":
    create_presentation()
