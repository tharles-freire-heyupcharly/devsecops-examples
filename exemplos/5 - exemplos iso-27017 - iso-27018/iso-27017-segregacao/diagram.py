#!/usr/bin/env python3
"""
ISO 27017 - Segregação de Ambientes
Diagrama mostrando isolamento de rede entre ambientes Dev e Prod
"""

from graphviz import Digraph

def create_segregation_diagram():
    """Cria diagrama de arquitetura de segregação ISO 27017"""
    
    dot = Digraph(comment='ISO 27017 - Segregação de Ambientes')
    dot.attr(rankdir='LR', splines='ortho', nodesep='1.0', ranksep='1.5')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    # Título
    dot.attr(label='ISO 27017 - Segregação de Ambientes\nIsolamento Completo: Dev ⊥ Prod', 
             fontsize='16', fontname='Arial Bold', labelloc='t')
    
    # ===== VPC Produção =====
    with dot.subgraph(name='cluster_prod') as c:
        c.attr(label='VPC Produção\n10.0.0.0/16\n[Environment=production]', 
               style='filled', color='#FFEBEE', fontsize='12')
        
        # Subnets
        c.node('prod_subnet1', 'Private Subnet 1\n10.0.1.0/24\nAZ: us-east-1a\n🔒', 
               fillcolor='#E74C3C', fontcolor='white')
        c.node('prod_subnet2', 'Private Subnet 2\n10.0.2.0/24\nAZ: us-east-1b\n🔒', 
               fillcolor='#E74C3C', fontcolor='white')
        
        # Resources
        c.node('prod_rds', 'RDS Production\n🗄️\nDados Críticos', 
               fillcolor='#527FFF', fontcolor='white', shape='cylinder')
        c.node('prod_ec2', 'EC2 Production\n💻\nCargas de Trabalho', 
               fillcolor='#FF9900', fontcolor='white')
        
        # NACL
        c.node('prod_nacl', 'Network ACL\n🚫\nDENY from 10.1.0.0/16', 
               fillcolor='#C0392B', fontcolor='white', shape='hexagon')
    
    # ===== VPC Desenvolvimento =====
    with dot.subgraph(name='cluster_dev') as c:
        c.attr(label='VPC Desenvolvimento\n10.1.0.0/16\n[Environment=development]', 
               style='filled', color='#E8F5E9', fontsize='12')
        
        # Subnets
        c.node('dev_subnet1', 'Private Subnet 1\n10.1.1.0/24\nAZ: us-east-1a\n🔒', 
               fillcolor='#27AE60', fontcolor='white')
        c.node('dev_subnet2', 'Private Subnet 2\n10.1.2.0/24\nAZ: us-east-1b\n🔒', 
               fillcolor='#27AE60', fontcolor='white')
        
        # Resources
        c.node('dev_rds', 'RDS Development\n🗄️\nDados de Teste', 
               fillcolor='#527FFF', fontcolor='white', shape='cylinder')
        c.node('dev_ec2', 'EC2 Development\n💻\nTestes', 
               fillcolor='#FF9900', fontcolor='white')
        
        # NACL
        c.node('dev_nacl', 'Network ACL\n🚫\nDENY from 10.0.0.0/16', 
               fillcolor='#229954', fontcolor='white', shape='hexagon')
    
    # ===== Conexões Internas (Permitidas) =====
    # Prod VPC
    dot.edge('prod_subnet1', 'prod_ec2', style='invis')
    dot.edge('prod_subnet2', 'prod_rds', style='invis')
    dot.edge('prod_ec2', 'prod_rds', label='✅ Allow\n(mesma VPC)', color='green', fontcolor='green')
    
    # Dev VPC
    dot.edge('dev_subnet1', 'dev_ec2', style='invis')
    dot.edge('dev_subnet2', 'dev_rds', style='invis')
    dot.edge('dev_ec2', 'dev_rds', label='✅ Allow\n(mesma VPC)', color='green', fontcolor='green')
    
    # ===== Tentativa de Conexão Bloqueada =====
    dot.edge('dev_ec2', 'prod_nacl', label='❌ DENIED\nNACL Rule', 
             color='red', style='dashed', fontcolor='red', constraint='false')
    dot.edge('prod_nacl', 'prod_rds', style='invis', constraint='false')
    
    dot.edge('prod_ec2', 'dev_nacl', label='❌ DENIED\nNACL Rule', 
             color='red', style='dashed', fontcolor='red', constraint='false')
    dot.edge('dev_nacl', 'dev_rds', style='invis', constraint='false')
    
    # ===== Internet Gateway (Separados) =====
    dot.node('igw_prod', 'Internet Gateway\n🌐\nProdução', 
             fillcolor='#3498DB', fontcolor='white', shape='house')
    dot.node('igw_dev', 'Internet Gateway\n🌐\nDesenvolvimento', 
             fillcolor='#5DADE2', fontcolor='white', shape='house')
    
    dot.edge('igw_prod', 'prod_subnet1', label='routed', style='dotted', dir='both')
    dot.edge('igw_dev', 'dev_subnet1', label='routed', style='dotted', dir='both')
    
    # ===== Security Groups =====
    with dot.subgraph(name='cluster_sg') as c:
        c.attr(label='Security Groups', style='filled', color='#FFF4E6')
        c.node('sg_prod', 'SG Production\n🛡️\nPort 443 only\nSource: VPC CIDR', 
               fillcolor='#E67E22', fontcolor='white', shape='octagon')
        c.node('sg_dev', 'SG Development\n🛡️\nPort 443, 22, 8080\nSource: VPC CIDR', 
               fillcolor='#F39C12', fontcolor='white', shape='octagon')
    
    dot.edge('sg_prod', 'prod_ec2', style='dotted', label='protects')
    dot.edge('sg_dev', 'dev_ec2', style='dotted', label='protects')
    
    # ===== Monitoramento =====
    dot.node('vpc_flow', 'VPC Flow Logs\n📊\nMonitora tentativas\nde acesso', 
             fillcolor='#9B59B6', fontcolor='white', shape='component')
    
    dot.edge('prod_nacl', 'vpc_flow', style='dotted', label='logs denials')
    dot.edge('dev_nacl', 'vpc_flow', style='dotted', label='logs denials')
    
    # Legenda
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Princípios de Segregação', style='filled', color='white')
        c.node('leg1', '🔴 CIDRs Não Sobrepostos:\n- Prod: 10.0.0.0/16\n- Dev: 10.1.0.0/16', 
               shape='note', fillcolor='#FFEBEE')
        c.node('leg2', '🟢 Isolamento de Rede:\n- Sem VPC Peering\n- NACLs bloqueiam inter-VPC\n- Zero trust entre ambientes', 
               shape='note', fillcolor='#E8F5E9')
        c.node('leg3', '⚠️ Blast Radius:\n- Incidente em Dev não afeta Prod\n- Dados de Prod inacessíveis de Dev', 
               shape='note', fillcolor='#FFF4E6')
    
    return dot

if __name__ == '__main__':
    diagram = create_segregation_diagram()
    diagram.attr(dpi='600')  # Alta resolução
    
    # Renderiza em PNG de altíssima qualidade
    diagram.render('iso-27017-segregacao-architecture', format='png', cleanup=True)
    print("✅ Diagrama PNG gerado: iso-27017-segregacao-architecture.png")
    
    # Renderiza em PDF vetorial
    diagram.render('iso-27017-segregacao-architecture', format='pdf', cleanup=True)
    print("✅ Diagrama PDF gerado: iso-27017-segregacao-architecture.pdf")
