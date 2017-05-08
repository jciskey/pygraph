"""Provides utility functions for unit testing."""

from ..pygraph import (DirectedGraph, UndirectedGraph,
                     build_triangle_graph, build_k5_graph, build_k33_graph, build_5_cycle_graph,
                     merge_graphs)


def build_simple_test_graph(directed=False):
    """Builds a simple undirected graph that gets used for testing."""
    if directed:
        graph = DirectedGraph()
    else:
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


def build_single_node_graph(directed=False):
    """Builds a graph with a single node for testing."""
    if directed:
        graph = DirectedGraph()
    else:
        graph = UndirectedGraph()
    graph.new_node()

    return graph


def build_2_node_graph(directed=False):
    """Builds a 2-node connected graph for testing."""
    if directed:
        graph = DirectedGraph()
    else:
        graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_edge(1, 2)

    return graph


def build_3_node_line_graph(directed=False):
    """Builds a 3-node, 2-edge connected line graph for testing."""
    if directed:
        graph = DirectedGraph()
    else:
        graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_node()

    graph.new_edge(1, 2)
    graph.new_edge(2, 3)

    return graph


def build_3_node_line_root_articulation_graph(directed=False):
    """Builds a 3-node, 2-edge connected line graph for testing, where the root node is the articulation vertex."""
    if directed:
        graph = DirectedGraph()
    else:
        graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_node()

    graph.new_edge(1, 2)
    graph.new_edge(1, 3)

    return graph


def build_biconnected_test_graph(directed=False):
    """Builds a graph with multiple biconnected components that gets used for testing."""
    if directed:
        graph = DirectedGraph()
    else:
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


def build_triangle_graph_with_costs(directed=False):
    """Builds a triangle graph with costs for testing."""
    if directed:
        graph = DirectedGraph()
    else:
        graph = UndirectedGraph()

    graph.new_node()
    graph.new_node()
    graph.new_node()

    graph.new_edge(1, 2, 1)
    graph.new_edge(2, 3, 2)
    graph.new_edge(3, 1, 10)

    return graph


def build_square_test_graph_with_costs(directed=False):
    """Builds a square graph with costs for testing."""
    if directed:
        graph = DirectedGraph()
    else:
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


def build_complicated_test_graph_with_one_mst(directed=False):
    """Builds a test graph that has a unique minimum spanning tree."""
    if directed:
        graph = DirectedGraph()
    else:
        graph = UndirectedGraph()

    for _ in xrange(7):
        graph.new_node()

    graph.new_edge(1, 2, 2)  # 1
    graph.new_edge(1, 3, 4)  # 2
    graph.new_edge(1, 4, 1)  # 3
    graph.new_edge(2, 4, 3)  # 4
    graph.new_edge(2, 5, 10)  # 5
    graph.new_edge(3, 4, 2)  # 6
    graph.new_edge(3, 6, 5)  # 7
    graph.new_edge(4, 5, 7)  # 8
    graph.new_edge(4, 6, 8)  # 9
    graph.new_edge(4, 7, 4)  # 10
    graph.new_edge(5, 7, 6)  # 11
    graph.new_edge(6, 7, 1)  # 12

    return graph


def build_non_planar_test_graph_with_k5_subgraph():
    """Builds a test graph that contains K5 as a subgraph, and is thus non-planar."""
    graph = build_triangle_graph()
    addition_graph = build_k5_graph()

    merge_graphs(graph, addition_graph)

    return graph


def build_non_planar_test_graph_with_k33_subgraph():
    """Builds a test graph that contains K3,3 as a subgraph, and is thus non-planar."""
    graph = build_triangle_graph()
    addition_graph = build_k33_graph()

    merge_graphs(graph, addition_graph)

    return graph


def build_non_planar_disconnected_test_graph_with_k5_subgraph():
    """Builds a disconnected test graph that contains K5 as a subgraph, and is thus non-planar."""
    graph = build_triangle_graph()
    addition_graph = build_k5_graph()
    addition_graph2 = build_k5_graph()

    merge_graphs(graph, addition_graph)
    merge_graphs(graph, addition_graph2)

    return graph


def build_petersons_graph():
    """Builds a non-planar test graph that does not contain K5 or K3,3 as a subgraph (Peterson's Graph).
       Ref: http://mathworld.wolfram.com/PetersenGraph.html"""
    graph = build_5_cycle_graph()

    # --Build a 5-pointed star
    for _ in xrange(5):
        graph.new_node()
    graph.new_edge(6, 8)
    graph.new_edge(6, 9)
    graph.new_edge(7, 9)
    graph.new_edge(7, 10)
    graph.new_edge(8, 10)

    # --Connect it to the outside 5-cycle graph
    graph.new_edge(1, 6)
    graph.new_edge(2, 7)
    graph.new_edge(3, 8)
    graph.new_edge(4, 9)
    graph.new_edge(5, 10)

    return graph
