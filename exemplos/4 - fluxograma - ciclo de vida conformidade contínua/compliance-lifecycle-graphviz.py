#!/usr/bin/env python3
"""
Gerador de Diagrama Profissional - Ciclo de Vida da Conformidade Automatizada
Usa Graphviz para criar diagramas de alta qualidade
"""

from graphviz import Digraph

def create_compliance_lifecycle_diagram():
    """Cria diagrama do ciclo de vida de compliance automatizada"""
    
    # Criar grafo
    dot = Digraph(comment='Ciclo de Vida da Conformidade Automatizada',
                  format='png',
                  engine='dot')
    
    # Configurações globais
    dot.attr(rankdir='LR',  # Left to Right
             splines='ortho',  # Linhas ortogonais
             nodesep='1.0',   # Aumentado para melhor espaçamento
             ranksep='1.5',   # Aumentado para melhor espaçamento
             fontname='Arial',
             bgcolor='white',
             dpi='1200',      # Aumentado para 1200 DPI (resolução gráfica profissional)
             resolution='1200')  # Força resolução máxima
    
    dot.attr('node', 
             shape='box',
             style='rounded,filled',
             fontname='Arial Bold',  # Fonte em negrito para melhor definição
             fontsize='18',   # Aumentado de 14 para 18
             width='3.2',     # Aumentado para acomodar texto maior
             height='2.4',    # Aumentado
             margin='0.5')
    
    dot.attr('edge',
             fontname='Arial Bold',
             fontsize='15',   # Aumentado de 12 para 15
             penwidth='3.5')  # Aumentado de 2.5 para 3.5
    
    # Nó inicial
    dot.node('start', '🚀\nInício',
             shape='circle',
             fillcolor='#e1f5e1',
             color='#4caf50',
             penwidth='4',    # Aumentado de 3
             width='2.0',     # Aumentado de 1.5
             height='2.0',    # Aumentado de 1.5
             fontsize='18',   # Aumentado de 14
             fontname='Arial Bold')
    
    # Fase 1 - DEFINIÇÃO
    dot.node('fase1', 
             '📋 1. DEFINIÇÃO\n\n' +
             'Requisitos Regulatórios\n↓\n' +
             'Tradução para Políticas\n↓\n' +
             'Rego, Sentinel, YAML',
             fillcolor='#e3f2fd',
             color='#2196f3',
             fontcolor='#000000')
    
    # Fase 2 - VERSIONAMENTO
    dot.node('fase2',
             '🔄 2. VERSIONAMENTO\n\n' +
             'Git: Controle de Versão\n↓\n' +
             'Code Review\n↓\n' +
             'Histórico Completo',
             fillcolor='#fff3e0',
             color='#ff9800',
             fontcolor='#000000')
    
    # Fase 3 - AUTOMAÇÃO CI/CD
    dot.node('fase3',
             '⚙️ 3. AUTOMAÇÃO CI/CD\n\n' +
             'Validação Automática\n↓\n' +
             'Cada Commit/PR/Deploy\n↓\n' +
             'OPA, Sentinel, Custodian',
             fillcolor='#f3e5f5',
             color='#9c27b0',
             fontcolor='#000000')
    
    # Fase 4 - ENFORCEMENT
    dot.node('fase4',
             '🛡️ 4. ENFORCEMENT\n\n' +
             'Bloqueia Deploys\n↓\n' +
             'Não Conformes\n↓\n' +
             'Remediação Automática',
             fillcolor='#fce4ec',
             color='#e91e63',
             fontcolor='#000000')
    
    # Fase 5 - AUDITORIA
    dot.node('fase5',
             '📊 5. AUDITORIA\n\n' +
             'Logs Automáticos\n↓\n' +
             'Dashboards Tempo Real\n↓\n' +
             'Evidências Regulatórias',
             fillcolor='#e0f2f1',
             color='#009688',
             fontcolor='#000000')
    
    # Nó final
    dot.node('end', '✅\nCompliance\nContínuo',
             shape='circle',
             fillcolor='#e1f5e1',
             color='#4caf50',
             penwidth='4',    # Aumentado de 3
             width='2.2',     # Aumentado de 1.8
             height='2.2',    # Aumentado de 1.8
             fontsize='17',   # Aumentado de 13
             fontname='Arial Bold')
    
    # Ferramentas
    dot.node('tools',
             '🔧 Ferramentas-chave\n\n' +
             'OPA | Sentinel | Kyverno\n' +
             'AWS Config | Azure Policy',
             fillcolor='#fff9c4',
             color='#fbc02d',
             fontcolor='#000000',
             shape='note',
             width='3.5',     # Aumentado de 3.0
             height='1.8',    # Aumentado de 1.5
             fontsize='16',   # Aumentado de 13
             fontname='Arial Bold')
    
    # Conexões principais (setas grossas)
    dot.edge('start', 'fase1', color='#4caf50', penwidth='4')      # Aumentado
    dot.edge('fase1', 'fase2', color='#2196f3', penwidth='4.5')    # Aumentado
    dot.edge('fase2', 'fase3', color='#ff9800', penwidth='4.5')    # Aumentado
    dot.edge('fase3', 'fase4', color='#9c27b0', penwidth='4.5')    # Aumentado
    dot.edge('fase4', 'fase5', color='#e91e63', penwidth='4.5')    # Aumentado
    dot.edge('fase5', 'end', color='#009688', penwidth='4')        # Aumentado
    
    # Feedback loop (pontilhado)
    dot.edge('end', 'fase1', 
             style='dashed',
             color='#666666',
             penwidth='3',   # Aumentado de 2
             constraint='false',
             label='Melhoria\nContínua')
    
    # Conexão para ferramentas
    dot.edge('fase5', 'tools',
             color='#fbc02d',
             penwidth='3',   # Aumentado de 2
             style='dotted')
    
    return dot

if __name__ == '__main__':
    # Gerar diagrama
    diagram = create_compliance_lifecycle_diagram()
    
    # Salvar em múltiplos formatos
    output_path = '/Users/tharles/Library/CloudStorage/GoogleDrive-tharles.freire@heyupcharly.com.br/My Drive/Fiap/Cloud Computing DevOps - DevSecOps/8SEG/compliance-lifecycle-graphviz'
    
    # PNG (ultra alta resolução - 1200 DPI)
    diagram.format = 'png'
    diagram.render(output_path, cleanup=True)
    print(f"✅ PNG gerado (1200 DPI): {output_path}.png")
    
    # SVG (vetorial - melhor para slides)
    diagram.format = 'svg'
    diagram.render(output_path, cleanup=True)
    print(f"✅ SVG gerado (vetorial): {output_path}.svg")
    
    # PDF (alta qualidade para impressão)
    diagram.format = 'pdf'
    diagram.render(output_path, cleanup=True)
    print(f"✅ PDF gerado: {output_path}.pdf")
    
    print("\n🎨 Diagramas gerados com sucesso!")
    print("   PNG: 1200 DPI - Resolução profissional de impressão gráfica")
    print("   SVG: Vetorial - Qualidade infinita, recomendado para PowerPoint")
    print("   PDF: Vetorial - Ideal para documentação e impressão")
    print("\n💡 DICA: Para melhor qualidade no PowerPoint, use o arquivo SVG!")
