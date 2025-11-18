#!/usr/bin/env python3
"""
ISO 27018 - Auditoria e Rastreabilidade
Diagrama mostrando arquitetura de auditoria completa com CloudTrail
"""

from graphviz import Digraph

def create_audit_diagram():
    """Cria diagrama de arquitetura de auditoria ISO 27018"""
    
    dot = Digraph(comment='ISO 27018 - Auditoria e Rastreabilidade')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='1.0')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    # Título
    dot.attr(label='ISO 27018 - Auditoria e Rastreabilidade\nLGPD Art. 37 | Retenção: 7 anos', 
             fontsize='16', fontname='Arial Bold', labelloc='t')
    
    # ===== Fontes de Dados Pessoais =====
    with dot.subgraph(name='cluster_datasources') as c:
        c.attr(label='Recursos com Dados Pessoais', style='filled', color='#FFF3E0')
        c.node('s3_pii', 'S3 Bucket\n📦\n[DataType=PII]\nCPF, Nome, Email', 
               fillcolor='#569A31', fontcolor='white')
        c.node('dynamo_pii', 'DynamoDB Table\n🗄️\n[DataType=PII]\nRegistros de usuários', 
               fillcolor='#527FFF', fontcolor='white')
        c.node('rds_pii', 'RDS Database\n💾\n[DataType=PII]\nDados financeiros', 
               fillcolor='#3B48CC', fontcolor='white')
    
    # ===== CloudTrail =====
    with dot.subgraph(name='cluster_cloudtrail') as c:
        c.attr(label='AWS CloudTrail', style='filled', color='#E3F2FD')
        c.node('trail', 'CloudTrail Trail\n📝\nMulti-Region: ✅\nValidation: ✅\nData Events: ✅', 
               fillcolor='#146EB4', fontcolor='white')
        c.node('events', 'Eventos Capturados\n🔍\n- GetObject (S3)\n- Query (DynamoDB)\n- SELECT (RDS)\n- IAM Changes', 
               fillcolor='#1E88E5', fontcolor='white')
    
    # ===== Armazenamento de Logs =====
    with dot.subgraph(name='cluster_storage') as c:
        c.attr(label='Armazenamento de Logs de Auditoria', style='filled', color='#E8F5E9')
        c.node('log_bucket', 'S3 Bucket (Logs)\n🗄️\nVersioning: ✅\nEncryption: AES-256\nMFA Delete: ✅', 
               fillcolor='#43A047', fontcolor='white')
        c.node('lifecycle', 'Lifecycle Policy\n♻️\nStandard: 90 dias\nGlacier: 7 anos\nDeleção: Após 7 anos', 
               fillcolor='#66BB6A', fontcolor='white')
    
    # ===== Detecção de Anomalias =====
    with dot.subgraph(name='cluster_detection') as c:
        c.attr(label='Detecção de Anomalias', style='filled', color='#FFF4E6')
        c.node('metric', 'CloudWatch Metric Filter\n📊\nDetecta:\n- Acesso fora de horário\n- Múltiplas falhas de acesso\n- Exportações em massa', 
               fillcolor='#FF4F8B', fontcolor='white')
        c.node('alarm', 'CloudWatch Alarm\n🚨\nThreshold: > 5 acessos/hora\nAvalia: 5 minutos', 
               fillcolor='#D4145A', fontcolor='white')
    
    # ===== Notificações =====
    with dot.subgraph(name='cluster_notifications') as c:
        c.attr(label='Alertas e Notificações', style='filled', color='#FFEBEE')
        c.node('sns', 'SNS Topic\n📧\nDestinatários:\n- Security Team\n- DPO (LGPD)', 
               fillcolor='#E74C3C', fontcolor='white')
        c.node('lambda', 'Lambda Function\n⚡\nEnriquece alertas\nCria tickets (JIRA)', 
               fillcolor='#FF9900', fontcolor='white')
    
    # ===== Análise e Compliance =====
    with dot.subgraph(name='cluster_analysis') as c:
        c.attr(label='Análise e Compliance', style='filled', color='#F3E5F5')
        c.node('athena', 'Amazon Athena\n🔎\nQueries SQL sobre logs\nRelatórios LGPD Art. 37', 
               fillcolor='#8E44AD', fontcolor='white')
        c.node('quicksight', 'QuickSight Dashboard\n📊\nVisualização:\n- Quem acessou?\n- Quando?\n- De onde?', 
               fillcolor='#9B59B6', fontcolor='white')
    
    # ===== Fluxo Principal =====
    # Acesso aos dados
    dot.edge('s3_pii', 'trail', label='1. Acesso auditado', color='blue', fontcolor='blue')
    dot.edge('dynamo_pii', 'trail', label='1. Acesso auditado', color='blue', fontcolor='blue')
    dot.edge('rds_pii', 'trail', label='1. Acesso auditado', color='blue', fontcolor='blue')
    
    # Trail → Eventos
    dot.edge('trail', 'events', label='2. Coleta eventos', color='blue', fontcolor='blue')
    
    # Eventos → Armazenamento
    dot.edge('events', 'log_bucket', label='3. Persiste logs', color='blue', fontcolor='blue')
    dot.edge('log_bucket', 'lifecycle', label='4. Aplica retenção', color='green', fontcolor='green')
    
    # Detecção
    dot.edge('events', 'metric', label='5. Analisa padrões', color='orange', fontcolor='orange', style='dashed')
    dot.edge('metric', 'alarm', label='6. Threshold excedido', color='red', fontcolor='red')
    
    # Alertas
    dot.edge('alarm', 'sns', label='7. Notifica', color='red', fontcolor='red')
    dot.edge('sns', 'lambda', label='8. Processa alerta', color='red', fontcolor='red')
    
    # Análise
    dot.edge('log_bucket', 'athena', label='9. Query logs', style='dotted')
    dot.edge('athena', 'quicksight', label='10. Visualiza', style='dotted')
    
    # ===== Validação de Integridade =====
    dot.node('validation', 'Log File Validation\n✅\nSHA-256 Hash\nDetecta adulteração', 
             fillcolor='#16A085', fontcolor='white', shape='diamond')
    dot.edge('log_bucket', 'validation', label='validate', style='dashed', color='green')
    
    # ===== Usuário/Administrador =====
    dot.node('user', 'Usuário/Admin\n👤\nAcessa dados pessoais', 
             fillcolor='#34495E', fontcolor='white', shape='person')
    dot.edge('user', 's3_pii', label='acessa', style='bold', color='purple')
    dot.edge('user', 'dynamo_pii', label='acessa', style='bold', color='purple')
    dot.edge('user', 'rds_pii', label='acessa', style='bold', color='purple')
    
    # Legenda
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Requisitos de Auditoria', style='filled', color='white')
        c.node('leg1', '✅ Multi-Region: Auditoria global\n✅ Data Events: Acesso a objetos/registros\n✅ Log Validation: Detecta adulteração', 
               shape='note', fillcolor='lightblue')
        c.node('leg2', '📋 LGPD Art. 37: Relatório de Impacto\n📋 Retenção: 7 anos mínimo\n📋 Não-repúdio: Prova de acesso', 
               shape='note', fillcolor='lightgreen')
        c.node('leg3', '🚨 Detecção: < 5 minutos\n🚨 Alertas: Security Team + DPO\n🚨 Resposta: Automática via Lambda', 
               shape='note', fillcolor='lightyellow')
    
    return dot

if __name__ == '__main__':
    diagram = create_audit_diagram()
    diagram.attr(dpi='600')  # Alta resolução
    
    # Renderiza em PNG de altíssima qualidade
    diagram.render('iso-27018-auditoria-architecture', format='png', cleanup=True)
    print("✅ Diagrama PNG gerado: iso-27018-auditoria-architecture.png")
    
    # Renderiza em PDF vetorial
    diagram.render('iso-27018-auditoria-architecture', format='pdf', cleanup=True)
    print("✅ Diagrama PDF gerado: iso-27018-auditoria-architecture.pdf")
