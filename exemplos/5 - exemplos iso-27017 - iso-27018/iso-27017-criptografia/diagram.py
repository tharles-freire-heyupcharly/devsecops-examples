#!/usr/bin/env python3
"""
ISO 27017 - Criptografia em Nuvem
Diagrama mostrando criptografia de dados em repouso com AWS KMS
"""

from graphviz import Digraph

def create_encryption_diagram():
    """Cria diagrama de arquitetura de criptografia ISO 27017"""
    
    dot = Digraph(comment='ISO 27017 - Criptografia em Nuvem')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.8', ranksep='1.0')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    # Título
    dot.attr(label='ISO 27017 - Criptografia de Dados em Repouso\nAES-256 | Rotação Automática', 
             fontsize='16', fontname='Arial Bold', labelloc='t')
    
    # ===== Aplicação/Usuário =====
    dot.node('app', 'Aplicação\n💻\nUpload de Dados', 
             fillcolor='#232F3E', fontcolor='white')
    
    # ===== AWS KMS =====
    with dot.subgraph(name='cluster_kms') as c:
        c.attr(label='AWS Key Management Service (KMS)', style='filled', color='#FFF4E6')
        c.node('cmk', 'Customer Master Key\n🔑\nRotação: 365 dias\nAlgorithm: AES-256', 
               fillcolor='#D4145A', fontcolor='white')
        c.node('dek', 'Data Encryption Keys\n🔐\nGeradas por CMK\nÚnicas por objeto', 
               fillcolor='#FF4F8B', fontcolor='white')
    
    # ===== S3 Bucket =====
    with dot.subgraph(name='cluster_s3') as c:
        c.attr(label='Amazon S3', style='filled', color='#E8F5E9')
        c.node('bucket', 'S3 Bucket\n📦\nserver_side_encryption', 
               fillcolor='#569A31', fontcolor='white')
        c.node('objects', 'Objetos Criptografados\n🔒\nAES-256-KMS\nMetadata: x-amz-server-side-encryption', 
               fillcolor='#7AC142', fontcolor='white')
    
    # ===== Controles de Segurança =====
    with dot.subgraph(name='cluster_security') as c:
        c.attr(label='Controles de Segurança', style='filled', color='#FFEBEE')
        c.node('block', 'Public Access Block\n🚫\nBloqueio Total', 
               fillcolor='#E74C3C', fontcolor='white')
        c.node('policy', 'Bucket Policy\n📜\nRequer Criptografia\nDeny sem KMS', 
               fillcolor='#C0392B', fontcolor='white')
    
    # ===== Auditoria =====
    with dot.subgraph(name='cluster_audit') as c:
        c.attr(label='Auditoria & Compliance', style='filled', color='#E3F2FD')
        c.node('cloudtrail', 'CloudTrail\n📋\nLogs de uso de chaves', 
               fillcolor='#146EB4', fontcolor='white')
        c.node('config', 'AWS Config\n⚙️\nValidação contínua', 
               fillcolor='#527FFF', fontcolor='white')
    
    # ===== Dados Descriptografados (Temporário) =====
    dot.node('decrypt', 'Dados Descriptografados\n🔓\nApenas em memória\nNunca em disco', 
             fillcolor='#95A5A6', fontcolor='white', shape='cylinder')
    
    # ===== Fluxo de Criptografia (Upload) =====
    dot.edge('app', 'bucket', label='1. PUT Object', color='blue', fontcolor='blue')
    dot.edge('bucket', 'cmk', label='2. Request DEK', color='blue', fontcolor='blue', style='dashed')
    dot.edge('cmk', 'dek', label='3. Generate', color='blue', fontcolor='blue')
    dot.edge('dek', 'bucket', label='4. Return DEK', color='blue', fontcolor='blue', style='dashed')
    dot.edge('bucket', 'objects', label='5. Encrypt & Store', color='blue', fontcolor='blue')
    
    # ===== Fluxo de Descriptografia (Download) =====
    dot.edge('app', 'objects', label='6. GET Object', color='green', fontcolor='green', dir='back')
    dot.edge('objects', 'cmk', label='7. Request Decrypt', color='green', fontcolor='green', 
             style='dashed', dir='forward')
    dot.edge('cmk', 'decrypt', label='8. Decrypt DEK', color='green', fontcolor='green')
    dot.edge('decrypt', 'app', label='9. Return Data', color='green', fontcolor='green')
    
    # ===== Controles =====
    dot.edge('block', 'bucket', label='prevents public access', style='dotted', color='red')
    dot.edge('policy', 'bucket', label='enforces encryption', style='dotted', color='red')
    
    # ===== Auditoria =====
    dot.edge('cmk', 'cloudtrail', label='logs key usage', style='dotted')
    dot.edge('bucket', 'config', label='compliance check', style='dotted')
    
    # ===== Rotação de Chaves =====
    dot.node('rotation', 'Rotação Automática\n♻️\n365 dias\nChaves antigas mantidas', 
             fillcolor='#F39C12', fontcolor='white', shape='diamond')
    dot.edge('cmk', 'rotation', label='auto-rotate', style='dashed', color='orange')
    
    # Legenda
    with dot.subgraph(name='cluster_legend') as c:
        c.attr(label='Detalhes de Implementação', style='filled', color='white')
        c.node('leg1', '🔵 Upload: Dados criptografados antes de armazenar\n🟢 Download: Dados descriptografados em memória', 
               shape='note', fillcolor='lightyellow')
        c.node('leg2', '✅ Criptografia: AES-256\n✅ Chaves gerenciadas pela AWS\n✅ Zero trust: Dados sempre criptografados em disco', 
               shape='note', fillcolor='lightgreen')
    
    return dot

if __name__ == '__main__':
    diagram = create_encryption_diagram()
    diagram.attr(dpi='600')  # Alta resolução
    
    # Renderiza em PNG de altíssima qualidade
    diagram.render('iso-27017-criptografia-architecture', format='png', cleanup=True)
    print("✅ Diagrama PNG gerado: iso-27017-criptografia-architecture.png")
    
    # Renderiza em PDF vetorial
    diagram.render('iso-27017-criptografia-architecture', format='pdf', cleanup=True)
    print("✅ Diagrama PDF gerado: iso-27017-criptografia-architecture.pdf")
