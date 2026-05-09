import graphviz



def method_flowchart() -> graphviz.Digraph:
    dot = graphviz.Digraph()
    dot.attr(
        size='7.0',
        rankdir='LR'
    )
    dot.attr(
        'node',
        shape='cylinder',
        fixedsize='true',
        width='1.8', 
        height='0.8'
    )
    dot.attr(
        'edge',
    )

    dot.edge('Análise Inicial', 'App Streamlit')
    dot.edge('Análise Inicial', 'Vídeo')

    dot.edge('App Streamlit', 'Teoria das Filas')
    dot.edge('Vídeo', 'Teoria das Filas')

    dot.edge('Teoria das Filas', 'Simulação M/M/s')
    dot.edge('Teoria das Filas', 'Simulação M/G/s')

    dot.edge('Simulação M/M/s', 'Resultados')
    dot.edge('Simulação M/G/s', 'Resultados')

    return dot


def service_area_flowchart() -> graphviz.Digraph:
    dot = graphviz.Digraph()
    dot.attr(
        size='6.5',
        rankdir='LR',
    )
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('R 1.8')
        s.node('R 2.8')
        s.node('R 3.8')
        s.node('R 4.8')
        s.node('R 5.8')
        s.node('R 6.8')

    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('R 1.4')
        s.node('R 2.4')
        s.node('R 3.4')
        s.node('R 4.4')
        s.node('R 5.4')
        s.node('R 6.4')

    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('Proteina 1')
        s.node('Proteina 2', group='g0')
        s.node('Proteina 3')

    dot.node('Catracas', group='g0')

    dot.node('Pratos 1', group='g1')
    dot.node('R 1.1', group='g1')
    dot.node('R 1.2', group='g1')
    dot.node('R 1.3', group='g1')
    dot.node('R 1.4', group='g1')
    dot.node('R 1.5', group='g1')
    dot.node('R 1.6', group='g1')
    dot.node('R 1.7', group='g1')
    dot.node('R 1.8', group='g1')

    dot.node('Pratos 2', group='g2')
    dot.node('R 2.1', group='g2')
    dot.node('R 2.2', group='g2')
    dot.node('R 2.3', group='g2')
    dot.node('R 2.4', group='g2')
    dot.node('R 2.5', group='g2')
    dot.node('R 2.6', group='g2')
    dot.node('R 2.7', group='g2')
    dot.node('R 2.8', group='g2')

    dot.node('Pratos 3', group='g3')
    dot.node('R 3.1', group='g3')
    dot.node('R 3.2', group='g3')
    dot.node('R 3.4', group='g3')
    dot.node('R 3.4', group='g3')
    dot.node('R 3.5', group='g3')
    dot.node('R 3.6', group='g3')
    dot.node('R 3.7', group='g3')
    dot.node('R 3.8', group='g3')

    dot.node('Pratos 4', group='g4')
    dot.node('R 4.1', group='g4')
    dot.node('R 4.2', group='g4')
    dot.node('R 4.4', group='g4')
    dot.node('R 4.4', group='g4')
    dot.node('R 4.5', group='g4')
    dot.node('R 4.6', group='g4')
    dot.node('R 4.7', group='g4')
    dot.node('R 4.8', group='g4')

    dot.node('Pratos 5', group='g5')
    dot.node('R 5.1', group='g5')
    dot.node('R 5.2', group='g5')
    dot.node('R 5.4', group='g5')
    dot.node('R 5.4', group='g5')
    dot.node('R 5.5', group='g5')
    dot.node('R 5.6', group='g5')
    dot.node('R 5.7', group='g5')
    dot.node('R 5.8', group='g5')

    dot.node('Pratos 6', group='g6')
    dot.node('R 6.1', group='g6')
    dot.node('R 6.2', group='g6')
    dot.node('R 6.4', group='g6')
    dot.node('R 6.4', group='g6')
    dot.node('R 6.5', group='g6')
    dot.node('R 6.6', group='g6')
    dot.node('R 6.7', group='g6')
    dot.node('R 6.8', group='g6')

    dot.node('Sobremesas', group='g0')
    dot.node('Mesas', group='g0')

    dot.edge('Catracas', 'Pratos 1')
    dot.edge('Catracas', 'Pratos 2')
    dot.edge('Catracas', 'Pratos 3')
    dot.edge('Catracas', 'Pratos 4')
    dot.edge('Catracas', 'Pratos 5')
    dot.edge('Catracas', 'Pratos 6')

    dot.edge('Pratos 1', 'R 1.1')
    dot.edge('R 1.1', 'R 1.2')
    dot.edge('R 1.2', 'R 1.3')
    dot.edge('R 1.3', 'R 1.4')
    dot.edge('R 1.4', 'Proteina 1')
    dot.edge('Proteina 1', 'R 1.5')
    dot.edge('R 1.5', 'R 1.6')
    dot.edge('R 1.6', 'R 1.7')
    dot.edge('R 1.7', 'R 1.8')

    dot.edge('Pratos 2', 'R 2.1')
    dot.edge('R 2.1', 'R 2.2')
    dot.edge('R 2.2', 'R 2.3')
    dot.edge('R 2.3', 'R 2.4')
    dot.edge('R 2.4', 'Proteina 1')
    dot.edge('Proteina 1', 'R 2.5')
    dot.edge('R 2.5', 'R 2.6')
    dot.edge('R 2.6', 'R 2.7')
    dot.edge('R 2.7', 'R 2.8')

    dot.edge('Pratos 3', 'R 3.1')
    dot.edge('R 3.1', 'R 3.2')
    dot.edge('R 3.2', 'R 3.3')
    dot.edge('R 3.3', 'R 3.4')
    dot.edge('R 3.4', 'Proteina 2')
    dot.edge('Proteina 2', 'R 3.5')
    dot.edge('R 3.5', 'R 3.6')
    dot.edge('R 3.6', 'R 3.7')
    dot.edge('R 3.7', 'R 3.8')

    dot.edge('Pratos 4', 'R 4.1')
    dot.edge('R 4.1', 'R 4.2')
    dot.edge('R 4.2', 'R 4.3')
    dot.edge('R 4.3', 'R 4.4')
    dot.edge('R 4.4', 'Proteina 2')
    dot.edge('Proteina 2', 'R 4.5')
    dot.edge('R 4.5', 'R 4.6')
    dot.edge('R 4.6', 'R 4.7')
    dot.edge('R 4.7', 'R 4.8')

    dot.edge('Pratos 5', 'R 5.1')
    dot.edge('R 5.1', 'R 5.2')
    dot.edge('R 5.2', 'R 5.3')
    dot.edge('R 5.3', 'R 5.4')
    dot.edge('R 5.4', 'Proteina 3')
    dot.edge('Proteina 3', 'R 5.5')
    dot.edge('R 5.5', 'R 5.6')
    dot.edge('R 5.6', 'R 5.7')
    dot.edge('R 5.7', 'R 5.8')

    dot.edge('Pratos 6', 'R 6.1')
    dot.edge('R 6.1', 'R 6.2')
    dot.edge('R 6.2', 'R 6.3')
    dot.edge('R 6.3', 'R 6.4')
    dot.edge('R 6.4', 'Proteina 3')
    dot.edge('Proteina 3', 'R 6.5')
    dot.edge('R 6.5', 'R 6.6')
    dot.edge('R 6.6', 'R 6.7')
    dot.edge('R 6.7', 'R 6.8')

    dot.edge('R 1.8', 'Mesas')
    dot.edge('R 2.8', 'Mesas')
    dot.edge('R 3.8', 'Mesas')
    dot.edge('R 4.8', 'Mesas')
    dot.edge('R 5.8', 'Mesas')
    dot.edge('R 6.8', 'Mesas')

    dot.edge('R 1.8', 'Sobremesas')
    dot.edge('R 2.8', 'Sobremesas')
    dot.edge('R 3.8', 'Sobremesas')
    dot.edge('R 4.8', 'Sobremesas')
    dot.edge('R 5.8', 'Sobremesas')
    dot.edge('R 6.8', 'Sobremesas')

    dot.edge('Sobremesas', 'Mesas')

    return dot

