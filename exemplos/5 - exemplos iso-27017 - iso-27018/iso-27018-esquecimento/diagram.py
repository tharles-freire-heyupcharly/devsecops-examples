#!/usr/bin/env python3
"""
ISO 27018 - Direito ao Esquecimento
Diagrama mostrando automação do Right to Erasure (LGPD Art. 18, VI)
"""

from graphviz import Digraph

def create_erasure_diagram():
    """Cria diagrama de arquitetura de direito ao esquecimento ISO 27018"""
    
    dot = Digraph(comment='ISO 27018 - Direito ao Esquecimento')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='1.0')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    # Título
    dot.attr(label='ISO 27018 - Direito ao Esquecimento (LGPD Art. 18, VI)\nPrazo: < 15 dias | SLA: 5 minutos', 
             fontsize='16', fontname='Arial Bold', labelloc='t')
    
    # ===== Titular de Dados =====
    dot.node('titular', 'Titular de Dados\n👤\nSolicitação de Exclusão\nLGPD Art. 18, VI', 
             fillcolor='#34495E', fontcolor='white', shape='person')
    
    # ===== Portal/API =====
    dot.node('api', 'API Gateway\n🌐\nPOST /data-erasure\n{"user_id": "12345"}', 
             fillcolor='#E67E22', fontcolor='white')
    
    # ===== Fila de Processamento =====
    with dot.subgraph(name='cluster_queue') as c:
        c.attr(label='Gerenciamento de Solicitações', style='filled', color='#FFF4E6')
        c.node('sqs', 'SQS Queue\n📬\nRetenção: 14 dias\nDLQ habilitada\nFIFO: ✅', 
               fillcolor='#D4145A', fontcolor='white')
        c.node('dlq', 'Dead Letter Queue\n⚠️\nFalhas após 3 tentativas', 
               fillcolor='#C0392B', fontcolor='white')
    
    # ===== Função Lambda =====
    with dot.subgraph(name='cluster_lambda') as c:
        c.attr(label='Processamento de Exclusão', style='filled', color='#FFE5CC')
        c.node('lambda_func', 'Lambda Function\n⚡\nTimeout: 5 min\nMemory: 1024 MB\nConcurrency: 10', 
               fillcolor='#FF9900', fontcolor='white')
        c.node('steps', 'Passos de Exclusão:\n1️⃣ Validar solicitação\n2️⃣ Excluir de S3\n3️⃣ Excluir de DynamoDB\n4️⃣ Excluir de RDS\n5️⃣ Registrar exclusão\n6️⃣ Notificar titular', 
               fillcolor='#FFB74D', fontcolor='black', shape='note')
    
    # ===== Fontes de Dados =====
    with dot.subgraph(name='cluster_datasources') as c:
        c.attr(label='Fontes de Dados Pessoais', style='filled', color='#E3F2FD')
        c.node('s3_data', 'S3 Bucket\n📦\nFotos, documentos', 
               fillcolor='#569A31', fontcolor='white')
        c.node('dynamo_data', 'DynamoDB\n🗄️\nPerfil de usuário', 
               fillcolor='#527FFF', fontcolor='white')
        c.node('rds_data', 'RDS Database\n💾\nTransações, histórico', 
               fillcolor='#3B48CC', fontcolor='white')
        c.node('elasticsearch', 'ElasticSearch\n🔍\nÍndices de busca', 
               fillcolor='#005571', fontcolor='white')
    
    # ===== Registro de Exclusões =====
    with dot.subgraph(name='cluster_registry') as c:
        c.attr(label='Auditoria de Exclusões (7 anos)', style='filled', color='#E8F5E9')
        c.node('audit_table', 'DynamoDB Audit Table\n📋\nPITR: ✅\nRegistro imutável:\n- user_id\n- timestamp\n- sistemas afetados\n- quem solicitou', 
               fillcolor='#43A047', fontcolor='white')
        c.node('cloudwatch', 'CloudWatch Logs\n📊\nRetenção: 7 anos\nLGPD Art. 37', 
               fillcolor='#66BB6A', fontcolor='white')
    
    # ===== Notificação ao Titular =====
    with dot.subgraph(name='cluster_notification') as c:
        c.attr(label='Confirmação ao Titular', style='filled', color='#F3E5F5')
        c.node('ses', 'Amazon SES\n📧\nEmail de confirmação\nComprovante de exclusão', 
               fillcolor='#8E44AD', fontcolor='white')
        c.node('sns_notify', 'SNS Topic\n📲\nNotifica DPO\nCompliance Team', 
               fillcolor='#9B59B6', fontcolor='white')
    
    # ===== Fluxo Principal =====
    # 1. Solicitação
    dot.edge('titular', 'api', label='1. POST request', color='blue', fontcolor='blue')
    dot.edge('api', 'sqs', label='2. Enqueue', color='blue', fontcolor='blue')
    
    # 2. Processamento
    dot.edge('sqs', 'lambda_func', label='3. Trigger', color='orange', fontcolor='orange')
    dot.edge('lambda_func', 'steps', style='invis')
    
    # 3. Exclusões
    dot.edge('lambda_func', 's3_data', label='4a. DELETE objects', color='red', fontcolor='red')
    dot.edge('lambda_func', 'dynamo_data', label='4b. DELETE items', color='red', fontcolor='red')
    dot.edge('lambda_func', 'rds_data', label='4c. DELETE rows', color='red', fontcolor='red')
    dot.edge('lambda_func', 'elasticsearch', label='4d. DELETE indices', color='red', fontcolor='red')
    
    # 4. Registro
    dot.edge('lambda_func', 'audit_table', label='5. Register erasure', color='green', fontcolor='green')
    dot.edge('lambda_func', 'cloudwatch', label='6. Log execution', color='green', fontcolor='green', style='dashed')
    
    # 5. Notificação
    dot.edge('lambda_func', 'ses', label='7a. Email titular', color='purple', fontcolor='purple')
    dot.edge('lambda_func', 'sns_notify', label='7b. Notify team', color='purple', fontcolor='purple')
    
    # 6. Falhas
    dot.edge('sqs', 'dlq', label='Após 3 falhas', color='red', fontcolor='red', style='dashed')
    
    # ===== Monitoramento =====
    dot.node('alarm', 'CloudWatch Alarm\n🚨\nMonitora:\n- DLQ depth > 0\n- Latência > 5 min\n- Taxa de erro > 1%', 
             fillcolor='#E74C3C', fontcolor='white', shape='diamond')
    dot.edge('dlq', 'alarm', label='triggers alert', color='red', style='dashed')
    dot.edge('cloudwatch', 'alarm', label='monitors', style='dotted')
    
    # ===== Confirmação ao Titular =====
    dot.edge('ses', 'titular', label='8. Confirmação\n"Seus dados foram excluídos"', 
             color='green', fontcolor='green', style='bold')
    
    # ===== Timeline =====
    with dot.subgraph(name='cluster_timeline') as c:
        c.attr(label='Timeline de Processamento', style='filled', color='#FFFDE7')
        c.node('timeline', 'T0: Solicitação recebida\n⏱️ T+2min: Exclusão de S3/DynamoDB\n⏱️ T+3min: Exclusão de RDS\n⏱️ T+4min: Registro de auditoria\n⏱️ T+5min: Confirmação enviada\n✅ SLA: < 15 dias (LGPD)', 
               shape='note', fillcolor='#FFF9C4')
    
    # Legenda
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Requisitos LGPD', style='filled', color='white')
        c.node('leg1', '✅ Art. 18, VI: Direito ao esquecimento\n✅ Art. 37: Auditoria por 7 anos\n✅ Prazo: Máximo 15 dias', 
               shape='note', fillcolor='lightgreen')
        c.node('leg2', '🔒 Garantias:\n- Processamento idempotente\n- Registro imutável (PITR)\n- Comprovante de exclusão\n- Rastreabilidade completa', 
               shape='note', fillcolor='lightblue')
        c.node('leg3', '⚠️ Multas evitadas:\n- Não atendimento: R$ 50 milhões\n- Sem comprovação: Sanções ANPD\n- Prazo excedido: Advertências', 
               shape='note', fillcolor='#FFCCBC')
    
    return dot

if __name__ == '__main__':
    diagram = create_erasure_diagram()
    diagram.attr(dpi='600')  # Alta resolução
    
    # Renderiza em PNG de altíssima qualidade
    diagram.render('iso-27018-esquecimento-architecture', format='png', cleanup=True)
    print("✅ Diagrama PNG gerado: iso-27018-esquecimento-architecture.png")
    
    # Renderiza em PDF vetorial
    diagram.render('iso-27018-esquecimento-architecture', format='pdf', cleanup=True)
    print("✅ Diagrama PDF gerado: iso-27018-esquecimento-architecture.pdf")
