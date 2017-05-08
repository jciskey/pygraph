"""Provides rendering capabilities for graphs."""


def graph_to_dot(graph, node_renderer=None, edge_renderer=None):
    """Produces a DOT specification string from the provided graph."""
    node_pairs = graph.nodes.items()
    edge_pairs = graph.edges.items()

    if node_renderer is None:
        node_renderer_wrapper = lambda nid: ''
    else:
        node_renderer_wrapper = lambda nid: ' [%s]' % ','.join(
            map(lambda tpl: '%s=%s' % tpl, node_renderer(graph, nid).items()))

    # Start the graph
    graph_string = 'digraph G {\n'
    graph_string += 'overlap=scale;\n'

    # Print the nodes (placeholder)
    for node_id, node in node_pairs:
        graph_string += '%i%s;\n' % (node_id, node_renderer_wrapper(node_id))

    # Print the edges
    for edge_id, edge in edge_pairs:
        node_a = edge['vertices'][0]
        node_b = edge['vertices'][1]
        graph_string += '%i -> %i;\n' % (node_a, node_b)

    # Finish the graph
    graph_string += '}'

    return graph_string