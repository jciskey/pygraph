"""Implements functions for planarity testing."""


from ..connected_components import get_connected_components_as_subgraphs
from ..biconnected_components import find_biconnected_components_as_subgraphs
from .kocay_algorithm import kocay_planarity_test


def is_planar(graph):
    """Determines whether a graph is planar or not."""
    # Determine connected components as subgraphs; their planarity is independent of each other
    connected_components = get_connected_components_as_subgraphs(graph)
    for component in connected_components:
        # Biconnected components likewise have independent planarity
        biconnected_components = find_biconnected_components_as_subgraphs(component)
        for bi_component in biconnected_components:
            planarity = __is_subgraph_planar(bi_component)
            if not planarity:
                return False
    return True


def __is_subgraph_planar(graph):
    """Internal function to determine if a subgraph is planar."""
    # --First pass: Determine edge and vertex counts validate Euler's Formula
    num_nodes = graph.num_nodes()
    num_edges = graph.num_edges()

    # --We can guarantee that if there are 4 or less nodes, then the graph is planar
    # --A 4-node simple graph has a maximum of 6 possible edges (K4); this will always satisfy Euler's Formula:
    # -- 6 <= 3(4 - 2)
    if num_nodes < 5:
        return True

    if num_edges > 3*(num_nodes - 2):
        return False

    # --At this point, we have no choice but to run the calculation the hard way
    return kocay_planarity_test(graph)


