#!/usr/bin/env python3
"""
Pipeline de Compliance Contínuo - GitHub Actions
Diagrama mostrando o fluxo completo de validação ISO 27017/27018
"""

from graphviz import Digraph

def create_compliance_pipeline_diagram():
    """Cria diagrama da pipeline de compliance contínuo"""
    
    dot = Digraph(comment='Pipeline de Compliance Contínuo')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.6', ranksep='0.8')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    # Título
    dot.attr(label='Pipeline de Compliance Contínuo - ISO 27017/27018\nGitHub Actions | Execução Diária às 3AM UTC', 
             fontsize='16', fontname='Arial Bold', labelloc='t')
    
    # ===== TRIGGERS =====
    with dot.subgraph(name='cluster_triggers') as c:
        c.attr(label='🎯 Triggers', style='filled', color='#E8F5E9')
        c.node('push', 'Push to main/develop\n📤', 
               fillcolor='#4CAF50', fontcolor='white', shape='cylinder')
        c.node('pr', 'Pull Request\n🔀', 
               fillcolor='#66BB6A', fontcolor='white', shape='cylinder')
        c.node('schedule', 'Schedule (Cron)\n⏰\nDiário 3AM UTC', 
               fillcolor='#81C784', fontcolor='white', shape='cylinder')
        c.node('manual', 'Manual Dispatch\n👆', 
               fillcolor='#A5D6A7', fontcolor='white', shape='cylinder')
    
    # ===== STAGE 1: Validação de Código =====
    with dot.subgraph(name='cluster_validation') as c:
        c.attr(label='STAGE 1: 📝 Validação de Código', style='filled', color='#E3F2FD')
        c.node('checkout1', 'Checkout Code\n📥', 
               fillcolor='#2196F3', fontcolor='white')
        c.node('tf_fmt', 'Terraform Format\n🎨\nterraform fmt -check', 
               fillcolor='#42A5F5', fontcolor='white')
        c.node('tf_validate', 'Terraform Validate\n✅\nterraform validate', 
               fillcolor='#64B5F6', fontcolor='white')
    
    # ===== STAGE 2: Análise de Segurança =====
    with dot.subgraph(name='cluster_security') as c:
        c.attr(label='STAGE 2: 🛡️ Análise de Segurança (SAST)', style='filled', color='#FFF3E0')
        c.node('tfsec', 'TFSec Scanner\n🔐\nVulnerabilidades', 
               fillcolor='#FF9800', fontcolor='white')
        c.node('checkov', 'Checkov\n🔍\nBest Practices', 
               fillcolor='#FFB74D', fontcolor='white')
        c.node('sarif', 'Upload SARIF\n📤\nGitHub Security', 
               fillcolor='#FFCC80', fontcolor='white')
    
    # ===== STAGE 3: Validação OPA =====
    with dot.subgraph(name='cluster_opa') as c:
        c.attr(label='STAGE 3: ⚖️ Validação de Políticas (OPA)', style='filled', color='#F3E5F5')
        c.node('opa_setup', 'Setup OPA\n🔧', 
               fillcolor='#9C27B0', fontcolor='white')
        c.node('policy_backup', 'ISO 27017\nBackup Policy\n💾', 
               fillcolor='#AB47BC', fontcolor='white', shape='folder')
        c.node('policy_crypto', 'ISO 27017\nEncryption Policy\n🔒', 
               fillcolor='#BA68C8', fontcolor='white', shape='folder')
        c.node('policy_network', 'ISO 27017\nNetwork Policy\n🌐', 
               fillcolor='#CE93D8', fontcolor='white', shape='folder')
        c.node('policy_audit', 'ISO 27018\nAudit Policy\n📋', 
               fillcolor='#E1BEE7', fontcolor='white', shape='folder')
        c.node('policy_erasure', 'ISO 27018\nErasure Policy\n🗑️', 
               fillcolor='#F3E5F5', fontcolor='black', shape='folder')
        c.node('policy_residency', 'ISO 27018\nResidency Policy\n🇧🇷', 
               fillcolor='#EDE7F6', fontcolor='black', shape='folder')
    
    # ===== STAGE 4: Terraform Plan =====
    with dot.subgraph(name='cluster_plan') as c:
        c.attr(label='STAGE 4: 📋 Terraform Plan', style='filled', color='#E0F2F1')
        c.node('tf_init', 'Terraform Init\n⚙️', 
               fillcolor='#00897B', fontcolor='white')
        c.node('tf_plan', 'Terraform Plan\n📋\nGera tfplan', 
               fillcolor='#26A69A', fontcolor='white')
        c.node('pr_comment', 'Comment on PR\n💬\nMostra mudanças', 
               fillcolor='#4DB6AC', fontcolor='white', shape='note')
    
    # ===== STAGE 5: Compliance Report =====
    with dot.subgraph(name='cluster_report') as c:
        c.attr(label='STAGE 5: 📊 Relatório de Compliance', style='filled', color='#FFF9C4')
        c.node('report_gen', 'Generate Report\n📊\nMarkdown', 
               fillcolor='#FBC02D', fontcolor='white')
        c.node('report_upload', 'Upload Artifact\n📤', 
               fillcolor='#FDD835', fontcolor='white')
        c.node('metrics', 'Métricas\n📈\n- Tempo execução\n- Violações\n- Conformidade', 
               fillcolor='#FFEB3B', fontcolor='black', shape='note')
    
    # ===== STAGE 6: Deploy =====
    with dot.subgraph(name='cluster_deploy') as c:
        c.attr(label='STAGE 6: 🚀 Deploy (Production)', style='filled', color='#FFEBEE')
        c.node('approval', 'Environment Approval\n✋\nProduction', 
               fillcolor='#D32F2F', fontcolor='white', shape='diamond')
        c.node('tf_apply', 'Terraform Apply\n🚀\n--auto-approve', 
               fillcolor='#E53935', fontcolor='white')
        c.node('verify', 'Verify Compliance\n✅\nPost-deployment', 
               fillcolor='#EF5350', fontcolor='white')
    
    # ===== STAGE 7: Notificações =====
    with dot.subgraph(name='cluster_notify') as c:
        c.attr(label='STAGE 7: 📧 Notificações', style='filled', color='#E8EAF6')
        c.node('slack', 'Slack Notification\n💬\nStatus da pipeline', 
               fillcolor='#5E35B1', fontcolor='white')
        c.node('email', 'Email DPO\n📧\nCompliance Team', 
               fillcolor='#7E57C2', fontcolor='white')
    
    # ===== Gate Decisions =====
    dot.node('gate1', 'Validação OK?', 
             fillcolor='#FFD54F', fontcolor='black', shape='diamond')
    dot.node('gate2', 'Segurança OK?', 
             fillcolor='#FFD54F', fontcolor='black', shape='diamond')
    dot.node('gate3', 'Políticas OK?', 
             fillcolor='#FFD54F', fontcolor='black', shape='diamond')
    dot.node('gate4', 'Plan OK?', 
             fillcolor='#FFD54F', fontcolor='black', shape='diamond')
    dot.node('gate5', 'Main Branch?', 
             fillcolor='#FFD54F', fontcolor='black', shape='diamond')
    
    # ===== Fluxo Principal =====
    # Triggers → Stage 1
    dot.edge('push', 'checkout1', color='green')
    dot.edge('pr', 'checkout1', color='green')
    dot.edge('schedule', 'checkout1', color='green')
    dot.edge('manual', 'checkout1', color='green')
    
    # Stage 1
    dot.edge('checkout1', 'tf_fmt', label='1')
    dot.edge('tf_fmt', 'tf_validate', label='2')
    dot.edge('tf_validate', 'gate1', label='3')
    
    # Stage 2
    dot.edge('gate1', 'tfsec', label='✅ PASS', color='green', fontcolor='green')
    dot.edge('tfsec', 'checkov', label='parallel', style='dashed')
    dot.edge('checkov', 'sarif')
    dot.edge('sarif', 'gate2')
    
    # Stage 3
    dot.edge('gate2', 'opa_setup', label='✅ PASS', color='green', fontcolor='green')
    dot.edge('opa_setup', 'policy_backup', label='validate')
    dot.edge('opa_setup', 'policy_crypto', label='validate')
    dot.edge('opa_setup', 'policy_network', label='validate')
    dot.edge('opa_setup', 'policy_audit', label='validate')
    dot.edge('opa_setup', 'policy_erasure', label='validate')
    dot.edge('opa_setup', 'policy_residency', label='validate')
    
    dot.edge('policy_backup', 'gate3', style='invis')
    dot.edge('policy_crypto', 'gate3', style='invis')
    dot.edge('policy_network', 'gate3', style='invis')
    dot.edge('policy_audit', 'gate3', style='invis')
    dot.edge('policy_erasure', 'gate3', style='invis')
    dot.edge('policy_residency', 'gate3')
    
    # Stage 4
    dot.edge('gate3', 'tf_init', label='✅ PASS', color='green', fontcolor='green')
    dot.edge('tf_init', 'tf_plan')
    dot.edge('tf_plan', 'pr_comment', label='if PR', style='dashed')
    dot.edge('tf_plan', 'gate4')
    
    # Stage 5
    dot.edge('gate4', 'report_gen', label='✅ PASS', color='green', fontcolor='green')
    dot.edge('report_gen', 'report_upload')
    dot.edge('report_gen', 'metrics', style='dotted')
    dot.edge('report_upload', 'gate5')
    
    # Stage 6
    dot.edge('gate5', 'approval', label='✅ main', color='green', fontcolor='green')
    dot.edge('approval', 'tf_apply', label='approved')
    dot.edge('tf_apply', 'verify')
    dot.edge('verify', 'slack')
    
    # Stage 7
    dot.edge('slack', 'email', label='parallel', style='dashed')
    
    # Falhas
    dot.node('failure', 'Pipeline Failed\n❌\nRollback', 
             fillcolor='#C62828', fontcolor='white', shape='octagon')
    dot.edge('gate1', 'failure', label='❌ FAIL', color='red', fontcolor='red', style='dashed')
    dot.edge('gate2', 'failure', label='❌ FAIL', color='red', fontcolor='red', style='dashed')
    dot.edge('gate3', 'failure', label='❌ FAIL', color='red', fontcolor='red', style='dashed')
    dot.edge('gate4', 'failure', label='❌ FAIL', color='red', fontcolor='red', style='dashed')
    dot.edge('failure', 'slack', label='notify', color='red')
    
    # Skip deploy em branches não-main
    dot.edge('gate5', 'slack', label='❌ não-main', color='orange', fontcolor='orange', style='dashed')
    
    # ===== Artefatos =====
    with dot.subgraph(name='cluster_artifacts') as c:
        c.attr(label='📦 Artefatos Gerados', style='filled', color='#F5F5F5')
        c.node('artifacts', '- Validation Report\n- Security SARIF\n- Policy Report\n- Terraform Plan\n- Compliance Report', 
               fillcolor='#BDBDBD', fontcolor='black', shape='folder')
    
    dot.edge('report_upload', 'artifacts', style='dotted')
    
    # ===== Métricas de SLA =====
    with dot.subgraph(name='cluster_sla') as c:
        c.attr(label='⏱️ SLA de Execução', style='filled', color='#E0F7FA')
        c.node('sla', 'Stage 1-2: ~3 min\nStage 3: ~5 min\nStage 4: ~2 min\nStage 5-6: ~1 min\n\n✅ Total: ~11 min', 
               fillcolor='#00ACC1', fontcolor='white', shape='note')
    
    # Legenda
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Legenda', style='filled', color='white')
        c.node('leg1', '🟢 Fluxo de Sucesso\n🔴 Fluxo de Falha\n🟠 Fluxo Condicional', 
               shape='note', fillcolor='lightyellow')
        c.node('leg2', '✅ Gates aprovados bloqueiam próximo stage\n❌ Falha em qualquer stage = rollback\n📧 Notificações sempre executam', 
               shape='note', fillcolor='lightblue')
        c.node('leg3', '🔒 Compliance:\n- ISO 27017 (Cloud Security)\n- ISO 27018 (Personal Data)\n- LGPD (Brasil)', 
               shape='note', fillcolor='lightgreen')
    
    return dot

if __name__ == '__main__':
    diagram = create_compliance_pipeline_diagram()
    diagram.attr(dpi='600')  # Alta resolução
    
    # Renderiza em PNG de altíssima qualidade
    diagram.render('compliance-pipeline-architecture', format='png', cleanup=True)
    print("✅ Diagrama PNG gerado: compliance-pipeline-architecture.png")
    
    # Renderiza em PDF vetorial
    diagram.render('compliance-pipeline-architecture', format='pdf', cleanup=True)
    print("✅ Diagrama PDF gerado: compliance-pipeline-architecture.pdf")
