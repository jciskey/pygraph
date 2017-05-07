"""Provides factory methods for building well-known, predefined graphs."""

from .classes import UndirectedGraph
from .helpers import create_graph_from_adjacency_matrix

def build_cycle_graph(num_nodes):
    """Builds a cycle graph with the specified number of nodes.
       Ref: http://mathworld.wolfram.com/CycleGraph.html"""
    graph = UndirectedGraph()

    if num_nodes > 0:
        first_node = graph.new_node()
        if num_nodes > 1:
            previous_node = first_node
            for _ in xrange(num_nodes - 1):
                new_node = graph.new_node()
                graph.new_edge(previous_node, new_node)
                previous_node = new_node
            graph.new_edge(previous_node, first_node)

    return graph


def build_wheel_graph(num_nodes):
    """Builds a wheel graph with the specified number of nodes.
       Ref: http://mathworld.wolfram.com/WheelGraph.html"""
    # The easiest way to build a wheel graph is to build
    # C_n-1 and then add a hub node and spoke edges
    graph = build_cycle_graph(num_nodes - 1)

    cycle_graph_vertices = graph.get_all_node_ids()

    node_id = graph.new_node()
    for cycle_node in cycle_graph_vertices:
        graph.new_edge(node_id, cycle_node)

    return graph

def build_triangle_graph():
    """Builds a triangle graph, C3.
       Ref: http://mathworld.wolfram.com/CycleGraph.html"""
    graph = build_cycle_graph(3)

    return graph


def build_square_graph():
    """Builds a square graph, C4.
       Ref: http://mathworld.wolfram.com/CycleGraph.html"""
    graph = build_cycle_graph(4)

    return graph


def build_diamond_graph():
    """Builds a diamond graph.
       Ref: http://mathworld.wolfram.com/DiamondGraph.html"""
    graph = build_square_graph()

    graph.new_edge(2, 4)

    return graph


def build_tetrahedral_graph():
    """Builds a tetrahedral graph, K4 (also, W4).
       Ref: http://mathworld.wolfram.com/TetrahedralGraph.html"""
    graph = build_wheel_graph(4)

    return graph


def build_5_cycle_graph():
    """Builds a 5-cycle graph, C5.
       Ref: http://mathworld.wolfram.com/CycleGraph.html"""
    graph = build_cycle_graph(5)

    return graph


def build_gem_graph():
    """Builds a gem graph, F4,1.
       Ref: http://mathworld.wolfram.com/GemGraph.html"""
    graph = build_5_cycle_graph()

    graph.new_edge(1, 3)
    graph.new_edge(1, 4)

    return graph


def build_k5_graph():
    """Makes a new K5 graph.
       Ref: http://mathworld.wolfram.com/Pentatope.html"""
    graph = UndirectedGraph()

    # K5 has 5 nodes
    for _ in xrange(5):
        graph.new_node()

    # K5 has 10 edges
    # --Edge: a
    graph.new_edge(1, 2)
    # --Edge: b
    graph.new_edge(2, 3)
    # --Edge: c
    graph.new_edge(3, 4)
    # --Edge: d
    graph.new_edge(4, 5)
    # --Edge: e
    graph.new_edge(5, 1)
    # --Edge: f
    graph.new_edge(1, 3)
    # --Edge: g
    graph.new_edge(1, 4)
    # --Edge: h
    graph.new_edge(2, 4)
    # --Edge: i
    graph.new_edge(2, 5)
    # --Edge: j
    graph.new_edge(3, 5)

    return graph


def build_k33_graph():
    """Makes a new K3,3 graph.
       Ref: http://mathworld.wolfram.com/UtilityGraph.html"""
    graph = UndirectedGraph()

    # K3,3 has 6 nodes
    for _ in xrange(1, 7):
        graph.new_node()

    # K3,3 has 9 edges
    # --Edge: a
    graph.new_edge(1, 4)
    # --Edge: b
    graph.new_edge(1, 5)
    # --Edge: c
    graph.new_edge(1, 6)
    # --Edge: d
    graph.new_edge(2, 4)
    # --Edge: e
    graph.new_edge(2, 5)
    # --Edge: f
    graph.new_edge(2, 6)
    # --Edge: g
    graph.new_edge(3, 4)
    # --Edge: h
    graph.new_edge(3, 5)
    # --Edge: i
    graph.new_edge(3, 6)

    return graph

def build_groetzch_graph():
    """Makes a new Groetzsch graph.
       Ref: http://mathworld.wolfram.com/GroetzschGraph.html"""
    # Because the graph is so complicated, we want to
    # build it via adjacency matrix specification
    
    # -- Initialize the matrix to all zeros
    adj = [[0 for _ in xrange(11)] for _ in xrange(11)]

    # -- Add individual edge connections
    row_connections = []

    row_connections.append( (1,2,7,10) )
    row_connections.append( (0,3,6,9) )
    row_connections.append( (0,4,6,8) )
    row_connections.append( (1,4,8,10) )
    row_connections.append( (2,3,7,9) )
    row_connections.append( (6,7,8,9,10) )
    row_connections.append( (1,2,5) )
    row_connections.append( (0,4,5) )
    row_connections.append( (2,3,5) )
    row_connections.append( (1,4,5) )
    row_connections.append( (0,3,5) )

    for j, tpl in enumerate(row_connections):
        for i in tpl:
            adj[j][i] = 1
            adj[i][j] = 1
    
    # Debug print the adjacency matrix
    #for row in adj:
    #    print row

    graph, _ = create_graph_from_adjacency_matrix(adj)

    return graph


def build_franklin_graph():
    """Makes a new Franklin graph.
       Ref: http://mathworld.wolfram.com/FranklinGraph.html"""
    # The easiest way to build the Franklin graph is to start
    # with C12 and add the additional 6 edges
    graph = build_cycle_graph(12)

    edge_tpls = [
        (1,8),
        (2,7),
        (3,10),
        (4,9),
        (5,12),
        (6,11)
    ]

    for i, j in edge_tpls:
        graph.new_edge(i, j)

    return graph


def build_chvatal_graph():
    """Makes a new Chvatal graph.
       Ref: http://mathworld.wolfram.com/ChvatalGraph.html"""
    # The easiest way to build the Chvatal graph is to start
    # with C12 and add the additional 12 edges
    graph = build_cycle_graph(12)

    edge_tpls = [
        (1,7), (1,9), (2,5), (2,11),
        (3,7), (3,9), (4,10), (4,12),
        (5,8), (6,10), (6,12), (8,11),
    ]

    for i, j in edge_tpls:
        graph.new_edge(i, j)

    return graph

