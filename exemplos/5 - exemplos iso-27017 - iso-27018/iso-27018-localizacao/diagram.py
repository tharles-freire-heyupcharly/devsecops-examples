#!/usr/bin/env python3
"""
ISO 27018 - Controle de Localização de Dados
Diagrama mostrando data residency e soberania de dados (LGPD)
"""

from graphviz import Digraph

def create_residency_diagram():
    """Cria diagrama de arquitetura de localização de dados ISO 27018"""
    
    dot = Digraph(comment='ISO 27018 - Controle de Localização de Dados')
    dot.attr(rankdir='TB', splines='ortho', nodesep='1.0', ranksep='1.2')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    # Título
    dot.attr(label='ISO 27018 - Data Residency (LGPD Art. 11 e 33)\nDados 100% em território brasileiro', 
             fontsize='16', fontname='Arial Bold', labelloc='t')
    
    # ===== Região Geográfica =====
    with dot.subgraph(name='cluster_brazil') as c:
        c.attr(label='🇧🇷 AWS sa-east-1 (São Paulo, Brasil)\nLatência: ~15ms | Compliance: LGPD', 
               style='filled,bold', color='#4CAF50', fontsize='14')
        
        # Availability Zones
        with c.subgraph(name='cluster_az1') as az:
            az.attr(label='AZ 1 (us-east-1a)', style='filled', color='#C8E6C9')
            az.node('s3_az1', 'S3 Bucket (Primary)\n📦\n[Region=sa-east-1]\n[LGPD=true]\n[DataType=PersonalData]', 
                    fillcolor='#569A31', fontcolor='white')
            az.node('rds_az1', 'RDS Primary\n💾\nMaster Instance', 
                    fillcolor='#527FFF', fontcolor='white')
        
        with c.subgraph(name='cluster_az2') as az:
            az.attr(label='AZ 2 (us-east-1b)', style='filled', color='#C8E6C9')
            az.node('s3_az2', 'S3 Replica (Local)\n📦\nSame Region Only', 
                    fillcolor='#7AC142', fontcolor='white')
            az.node('rds_az2', 'RDS Standby\n💾\nRead Replica', 
                    fillcolor='#7B9FFF', fontcolor='white')
        
        # Bucket Policy
        c.node('policy', 'Bucket Policy\n🚫\nDENY Replication\nfora de sa-east-1', 
               fillcolor='#E74C3C', fontcolor='white', shape='octagon')
        
        # Lifecycle
        c.node('lifecycle', 'Lifecycle Policy\n♻️\nRetenção máxima: 5 anos\nLGPD Art. 15', 
               fillcolor='#F39C12', fontcolor='white')
    
    # ===== Regiões Bloqueadas =====
    with dot.subgraph(name='cluster_blocked') as c:
        c.attr(label='❌ Regiões Bloqueadas (Replicação Proibida)', 
               style='filled,dashed', color='#FFCDD2', fontsize='12')
        c.node('us_east', 'US East (N. Virginia)\n🇺🇸\nus-east-1', 
               fillcolor='#B0BEC5', fontcolor='black', style='filled,dashed')
        c.node('eu_west', 'EU West (Ireland)\n🇮🇪\neu-west-1', 
               fillcolor='#B0BEC5', fontcolor='black', style='filled,dashed')
        c.node('ap_south', 'AP South (Singapore)\n🇸🇬\nap-southeast-1', 
               fillcolor='#B0BEC5', fontcolor='black', style='filled,dashed')
    
    # ===== AWS Config =====
    with dot.subgraph(name='cluster_monitoring') as c:
        c.attr(label='Monitoramento de Compliance', style='filled', color='#E3F2FD')
        c.node('config', 'AWS Config\n⚙️\nRegra: s3-bucket-replication-enabled\nAction: DENY cross-region', 
               fillcolor='#146EB4', fontcolor='white')
        c.node('config_rule', 'Config Rule\n📋\nVerifica:\n- Region = sa-east-1\n- Tags: LGPD=true\n- No cross-region replication', 
               fillcolor='#1E88E5', fontcolor='white')
    
    # ===== CloudWatch Alarms =====
    with dot.subgraph(name='cluster_alarms') as c:
        c.attr(label='Alertas de Violação', style='filled', color='#FFF4E6')
        c.node('alarm', 'CloudWatch Alarm\n🚨\nDetecta tentativas de:\n- Cross-region replication\n- Data export fora do Brasil', 
               fillcolor='#D4145A', fontcolor='white')
        c.node('sns', 'SNS Topic\n📧\nNotifica:\n- DPO\n- Compliance Officer\n- Security Team', 
               fillcolor='#FF4F8B', fontcolor='white')
    
    # ===== Usuários =====
    dot.node('user_br', 'Usuários no Brasil\n👥\nLatência: ~15ms\nAcesso direto', 
             fillcolor='#4CAF50', fontcolor='white', shape='person')
    dot.node('user_global', 'Usuários Globais\n🌍\nLatência: variável\nDados permanecem no Brasil', 
             fillcolor='#FF9800', fontcolor='white', shape='person')
    
    # ===== Fluxo de Dados =====
    # Acesso local (permitido)
    dot.edge('user_br', 's3_az1', label='✅ Acesso permitido\nDados em sa-east-1', 
             color='green', fontcolor='green', style='bold')
    dot.edge('user_global', 's3_az1', label='✅ Acesso permitido\nDados NÃO saem do Brasil', 
             color='orange', fontcolor='orange', style='bold')
    
    # Replicação local (permitida)
    dot.edge('s3_az1', 's3_az2', label='✅ Replicação permitida\n(mesma região)', 
             color='green', fontcolor='green', dir='both')
    dot.edge('rds_az1', 'rds_az2', label='✅ Replicação permitida\n(mesma região)', 
             color='green', fontcolor='green', dir='both')
    
    # Replicação cross-region (bloqueada)
    dot.edge('s3_az1', 'us_east', label='❌ DENIED\nBucket Policy', 
             color='red', fontcolor='red', style='dashed')
    dot.edge('s3_az1', 'eu_west', label='❌ DENIED\nBucket Policy', 
             color='red', fontcolor='red', style='dashed')
    dot.edge('s3_az1', 'ap_south', label='❌ DENIED\nBucket Policy', 
             color='red', fontcolor='red', style='dashed')
    
    # Controles
    dot.edge('policy', 's3_az1', label='enforces', style='dotted', color='red')
    dot.edge('lifecycle', 's3_az1', label='manages retention', style='dotted', color='orange')
    
    # Monitoramento
    dot.edge('config', 's3_az1', label='validates compliance', style='dotted')
    dot.edge('config', 'config_rule', style='invis')
    dot.edge('config_rule', 'alarm', label='triggers on violation', color='red', style='dashed')
    dot.edge('alarm', 'sns', label='notifies', color='red')
    
    # ===== Certificação =====
    with dot.subgraph(name='cluster_cert') as c:
        c.attr(label='Certificações e Compliance', style='filled', color='#F3E5F5')
        c.node('certs', 'Conformidade:\n✅ LGPD Art. 11 (Transferência)\n✅ LGPD Art. 33 (Localização)\n✅ ISO 27018\n✅ SOC 2 Type II', 
               fillcolor='#9B59B6', fontcolor='white', shape='folder')
    
    # ===== Logs e Auditoria =====
    dot.node('cloudtrail', 'CloudTrail\n📋\nRegistra:\n- Tentativas de replicação\n- Exportações de dados\n- Mudanças em policies', 
             fillcolor='#146EB4', fontcolor='white')
    dot.edge('s3_az1', 'cloudtrail', label='audit trail', style='dotted')
    
    # ===== Latência e Performance =====
    with dot.subgraph(name='cluster_performance') as c:
        c.attr(label='Métricas de Performance', style='filled', color='#FFFDE7')
        c.node('metrics', 'Latência por Região:\n🇧🇷 Brasil: ~15ms\n🇺🇸 EUA: ~150ms\n🇪🇺 Europa: ~180ms\n🇸🇬 Ásia: ~250ms\n\n✅ Trade-off aceito para compliance LGPD', 
               shape='note', fillcolor='#FFF9C4')
    
    # Legenda
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Garantias de Localização', style='filled', color='white')
        c.node('leg1', '🇧🇷 100% dos dados em sa-east-1 (Brasil)\n🚫 Zero replicação cross-region\n✅ Multi-AZ para alta disponibilidade', 
               shape='note', fillcolor='lightgreen')
        c.node('leg2', '📋 LGPD Art. 11: Transferência internacional proibida\n📋 LGPD Art. 33: Localização deve ser informada\n📋 Retenção: Máximo 5 anos (LGPD Art. 15)', 
               shape='note', fillcolor='lightblue')
        c.node('leg3', '⚠️ Violações detectadas:\n- Tentativa de replicação → Alerta imediato\n- Export para outra região → Bloqueado\n- Policy modificada → Auditoria', 
               shape='note', fillcolor='#FFCCBC')
    
    return dot

if __name__ == '__main__':
    diagram = create_residency_diagram()
    diagram.attr(dpi='600')  # Alta resolução
    
    # Renderiza em PNG de altíssima qualidade
    diagram.render('iso-27018-localizacao-architecture', format='png', cleanup=True)
    print("✅ Diagrama PNG gerado: iso-27018-localizacao-architecture.png")
    
    # Renderiza em PDF vetorial
    diagram.render('iso-27018-localizacao-architecture', format='pdf', cleanup=True)
    print("✅ Diagrama PDF gerado: iso-27018-localizacao-architecture.pdf")
