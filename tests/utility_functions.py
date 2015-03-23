"""Provides utility functions for unit testing."""

from ..graph import UndirectedGraph, build_triangle_graph, merge_graphs


def build_simple_test_graph():
    """Builds a simple undirected graph that gets used for testing."""
    graph = UndirectedGraph()

    # There are 7 vertices in the test graph
    for _ in xrange(7):
        graph.new_node()

    # There are 4 edges in the test graph
    # --Edge: a
    graph.new_edge(1, 2)
    # --Edge: b
    graph.new_edge(1, 4)
    # --Edge: c
    graph.new_edge(2, 5)
    # --Edge: d
    graph.new_edge(6, 7)

    return graph


def build_single_node_graph():
    """Builds a graph with a single node for testing."""
    graph = UndirectedGraph()
    graph.new_node()

    return graph


def build_2_node_graph():
    """Builds a 2-node connected graph for testing."""
    graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_edge(1, 2)

    return graph


def build_3_node_line_graph():
    """Builds a 3-node, 2-edge connected line graph for testing."""
    graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_node()

    graph.new_edge(1, 2)
    graph.new_edge(2, 3)

    return graph


def build_3_node_line_root_articulation_graph():
    """Builds a 3-node, 2-edge connected line graph for testing, where the root node is the articulation vertex."""
    graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_node()

    graph.new_edge(1, 2)
    graph.new_edge(1, 3)

    return graph


def build_biconnected_test_graph():
    """Builds a graph with multiple biconnected components that gets used for testing."""
    graph = UndirectedGraph()

    # There are 12 vertices in the test graph
    for _ in xrange(12):
        graph.new_node()

    # Nodes 1,2,3 form the first component
    graph.new_edge(1, 2)
    graph.new_edge(1, 3)
    graph.new_edge(2, 3)

    # Nodes 4,5,6,7 form the second component
    graph.new_edge(4, 5)
    graph.new_edge(4, 6)
    graph.new_edge(5, 6)
    graph.new_edge(5, 7)
    graph.new_edge(6, 7)

    # Nodes 8,9,10,11,12 form the third component
    graph.new_edge(8, 9)
    graph.new_edge(8, 10)
    graph.new_edge(8, 11)
    graph.new_edge(8, 12)
    graph.new_edge(9, 10)
    graph.new_edge(10, 11)
    graph.new_edge(10, 12)
    graph.new_edge(11, 12)

    # Nodes 2 and 5 connect the first and second components
    graph.new_edge(2, 5)

    # Nodes 7 and 8 connect the second and third components
    graph.new_edge(7, 8)

    return graph


def build_fully_biconnected_test_graph():
    """Builds a graph with only one biconnected component that gets used for testing."""
    graph = build_biconnected_test_graph()

    # Connect the first and third components to create a ring, converting everything into a single biconnected component
    graph.new_edge(1, 12)

    return graph


def build_disconnected_test_graph():
    """Builds a graph with three disconnected components that gets used for testing."""
    graph = build_triangle_graph()
    g2 = build_triangle_graph()
    g3 = build_triangle_graph()

    merge_graphs(graph, g2)
    merge_graphs(graph, g3)

    return graph


def build_triangle_graph_with_costs():
    """Builds a triangle graph with costs for testing."""
    graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_node()

    graph.new_edge(1, 2, 1)
    graph.new_edge(2, 3, 2)
    graph.new_edge(3, 1, 10)

    return graph

def build_square_test_graph_with_costs():
    """Builds a square graph with costs for testing."""
    graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_node()
    graph.new_node()
    graph.new_edge(1, 2, 2)
    graph.new_edge(1, 4, 10)
    graph.new_edge(2, 3, 3)
    graph.new_edge(3, 4, 1)

    return graph

def build_complicated_test_graph_with_one_mst():
    """Builds a test graph that has a unique minimum spanning tree."""
    graph = UndirectedGraph()

    for _ in xrange(7):
        graph.new_node()

    graph.new_edge(1, 2, 2)  # 1
    graph.new_edge(1, 3, 4)  # 2
    graph.new_edge(1, 4, 1)  # 3
    graph.new_edge(2, 4, 3)  # 4
    graph.new_edge(2, 5, 10)  #5
    graph.new_edge(3, 4, 2)  # 6
    graph.new_edge(3, 6, 5)  # 7
    graph.new_edge(4, 5, 7)  # 8
    graph.new_edge(4, 6, 8)  # 9
    graph.new_edge(4, 7, 4)  # 10
    graph.new_edge(5, 7, 6)  # 11
    graph.new_edge(6, 7, 1)  # 12

    return graph