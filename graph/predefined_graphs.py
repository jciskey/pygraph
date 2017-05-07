"""Provides factory methods for building well-known, predefined graphs."""

from .classes import UndirectedGraph

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
    """Builds a tetrahedral graph.
       Ref: http://mathworld.wolfram.com/TetrahedralGraph.html"""
    graph = build_triangle_graph()

    graph.new_node()
    graph.new_edge(1, 4)
    graph.new_edge(2, 4)
    graph.new_edge(3, 4)

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

