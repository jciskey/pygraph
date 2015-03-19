"""Provides factory methods for building well-known, predefined graphs."""

from .classes import UndirectedGraph


def build_triangle_graph():
    """Builds a triangle graph."""
    graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_node()
    graph.new_edge(1, 2)
    graph.new_edge(1, 3)
    graph.new_edge(2, 3)

    return graph


def build_square_graph():
    """Builds a square graph."""
    graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_node()
    graph.new_node()
    graph.new_edge(1, 2)
    graph.new_edge(1, 4)
    graph.new_edge(2, 3)
    graph.new_edge(3, 4)

    return graph


def build_diamond_graph():
    """Builds a diamond graph."""
    graph = build_square_graph()

    graph.new_edge(2, 4)

    return graph


def build_tetrahedral_graph():
    """Builds a tetrahedral graph."""
    graph = build_triangle_graph()

    graph.new_node()
    graph.new_edge(1, 4)
    graph.new_edge(2, 4)
    graph.new_edge(3, 4)

    return graph


def build_5_cycle_graph():
    """Builds a 5-cycle graph."""
    graph = UndirectedGraph()

    for _ in xrange(5):
        graph.new_node()

    graph.new_edge(1, 2)
    graph.new_edge(2, 3)
    graph.new_edge(3, 4)
    graph.new_edge(4, 5)
    graph.new_edge(5, 1)

    return graph


def build_gem_graph():
    """Builds a gem graph."""
    graph = build_5_cycle_graph()

    graph.new_edge(1, 3)
    graph.new_edge(1, 4)

    return graph


def build_k5_graph():
    """Makes a new K5 graph."""
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
    """Makes a new K3,3 graph."""
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

