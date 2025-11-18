#!/usr/bin/env python3
"""
ISO 27017 - Backup e Recuperação
Diagrama mostrando arquitetura de backup automatizado com AWS Backup
"""

from graphviz import Digraph

def create_backup_diagram():
    """Cria diagrama de arquitetura de backup ISO 27017"""
    
    dot = Digraph(comment='ISO 27017 - Backup e Recuperação')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='1.0')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    # Título
    dot.attr(label='ISO 27017 - Backup e Recuperação\nRPO: 24h | RTO: < 4h', 
             fontsize='16', fontname='Arial Bold', labelloc='t')
    
    # ===== Camada de Recursos Protegidos =====
    with dot.subgraph(name='cluster_resources') as c:
        c.attr(label='Recursos Protegidos', style='filled', color='lightgray')
        c.node('ec2', 'EC2 Instances\n💻\n[Environment=production]', 
               fillcolor='#FF9900', fontcolor='white')
        c.node('ebs', 'EBS Volumes\n💾\n[BackupRequired=true]', 
               fillcolor='#FF9900', fontcolor='white')
        c.node('rds', 'RDS Databases\n🗄️\n[Critical Data]', 
               fillcolor='#527FFF', fontcolor='white')
    
    # ===== AWS Backup Service =====
    with dot.subgraph(name='cluster_backup') as c:
        c.attr(label='AWS Backup Service', style='filled', color='#E7F3FF')
        c.node('selection', 'Backup Selection\n🏷️\nPor Tags', 
               fillcolor='#146EB4', fontcolor='white')
        c.node('plan', 'Backup Plan\n📅\nDiário 3AM UTC\nRetenção: 30 dias', 
               fillcolor='#146EB4', fontcolor='white')
        c.node('vault', 'Backup Vault\n🔒\nCofre Isolado\nCriptografado', 
               fillcolor='#146EB4', fontcolor='white')
    
    # ===== Camada de Armazenamento =====
    with dot.subgraph(name='cluster_storage') as c:
        c.attr(label='Armazenamento de Backup', style='filled', color='#F0F0F0')
        c.node('s3', 'S3 (Cold Storage)\n❄️\nBackups Compactados', 
               fillcolor='#569A31', fontcolor='white')
        c.node('snapshots', 'EBS/RDS Snapshots\n📸\nIncremental', 
               fillcolor='#569A31', fontcolor='white')
    
    # ===== Monitoramento e Alertas =====
    with dot.subgraph(name='cluster_monitoring') as c:
        c.attr(label='Monitoramento', style='filled', color='#FFF4E6')
        c.node('sns', 'SNS Topic\n📧\nAlertas', 
               fillcolor='#D4145A', fontcolor='white')
        c.node('cloudwatch', 'CloudWatch\n📊\nMétricas & Logs', 
               fillcolor='#FF4F8B', fontcolor='white')
    
    # ===== Recovery =====
    dot.node('recovery', 'Recovery Process\n♻️\nRestauração sob demanda', 
             fillcolor='#232F3E', fontcolor='white')
    
    # ===== Conexões =====
    # Recursos → Seleção
    dot.edge('ec2', 'selection', label='monitored by')
    dot.edge('ebs', 'selection', label='monitored by')
    dot.edge('rds', 'selection', label='monitored by')
    
    # Seleção → Plano → Vault
    dot.edge('selection', 'plan', label='triggers')
    dot.edge('plan', 'vault', label='executes')
    
    # Vault → Armazenamento
    dot.edge('vault', 's3', label='stores in')
    dot.edge('vault', 'snapshots', label='creates')
    
    # Vault → Monitoramento
    dot.edge('vault', 'sns', label='notifies', style='dashed', color='red')
    dot.edge('vault', 'cloudwatch', label='logs to', style='dashed')
    
    # Recovery
    dot.edge('vault', 'recovery', label='restore from', 
             color='green', style='bold', dir='both')
    
    # Legenda
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Legenda', style='filled', color='white')
        c.node('leg1', '🏷️ Seleção por Tags\n📅 Agendamento Automático\n🔒 Criptografia AES-256', 
               shape='note', fillcolor='lightyellow')
        c.node('leg2', '✅ RPO: 24h (backup diário)\n✅ RTO: < 4h (recovery rápido)\n✅ Retenção: 30 dias', 
               shape='note', fillcolor='lightgreen')
    
    return dot

if __name__ == '__main__':
    diagram = create_backup_diagram()
    diagram.attr(dpi='600')  # Alta resolução
    
    # Renderiza em PNG de altíssima qualidade
    diagram.render('iso-27017-backup-architecture', format='png', cleanup=True)
    print("✅ Diagrama PNG gerado: iso-27017-backup-architecture.png")
    
    # Renderiza em PDF vetorial
    diagram.render('iso-27017-backup-architecture', format='pdf', cleanup=True)
    print("✅ Diagrama PDF gerado: iso-27017-backup-architecture.pdf")
