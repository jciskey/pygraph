"""Implements a minimum spanning tree algorithm."""

from ..exceptions import DisconnectedGraphError
from .connected_components import get_connected_components, get_connected_components_as_subgraphs
from ..helpers import DisjointSet, PriorityQueue, get_subgraph_from_edge_list


def find_minimum_spanning_tree(graph):
    """Calculates a minimum spanning tree for a graph.
    Returns a list of edges that define the tree.
    Returns an empty list for an empty graph.
    """
    mst = []

    if graph.num_nodes() == 0:
        return mst
    if graph.num_edges() == 0:
        return mst

    connected_components = get_connected_components(graph)
    if len(connected_components) > 1:
        raise DisconnectedGraphError

    edge_list = kruskal_mst(graph)

    return edge_list


def find_minimum_spanning_tree_as_subgraph(graph):
    """Calculates a minimum spanning tree and returns a graph representation."""
    edge_list = find_minimum_spanning_tree(graph)
    subgraph = get_subgraph_from_edge_list(graph, edge_list)

    return subgraph


def find_minimum_spanning_forest(graph):
    """Calculates the minimum spanning forest of a disconnected graph.
    Returns a list of lists, each containing the edges that define that tree.
    Returns an empty list for an empty graph.
    """
    msf = []

    if graph.num_nodes() == 0:
        return msf
    if graph.num_edges() == 0:
        return msf

    connected_components = get_connected_components_as_subgraphs(graph)
    for subgraph in connected_components:
        edge_list = kruskal_mst(subgraph)
        msf.append(edge_list)

    return msf


def find_minimum_spanning_forest_as_subgraphs(graph):
    """Calculates the minimum spanning forest and returns a list of trees as subgraphs."""
    forest = find_minimum_spanning_forest(graph)
    list_of_subgraphs = map(lambda edge_list: get_subgraph_from_edge_list(graph, edge_list), forest)

    return list_of_subgraphs


def kruskal_mst(graph):
    """Implements Kruskal's Algorithm for finding minimum spanning trees.
    Assumes a non-empty, connected graph.
    """
    edges_accepted = 0
    ds = DisjointSet()
    pq = PriorityQueue()
    accepted_edges = []
    label_lookup = {}

    nodes = graph.get_all_node_ids()
    num_vertices = len(nodes)
    for n in nodes:
        label = ds.add_set()
        label_lookup[n] = label

    edges = graph.get_all_edge_objects()
    for e in edges:
        pq.put(e['id'], e['cost'])

    while edges_accepted < (num_vertices - 1):
        edge_id = pq.get()

        edge = graph.get_edge(edge_id)
        node_a, node_b = edge['vertices']
        label_a = label_lookup[node_a]
        label_b = label_lookup[node_b]

        a_set = ds.find(label_a)
        b_set = ds.find(label_b)

        if a_set != b_set:
            edges_accepted += 1
            accepted_edges.append(edge_id)
            ds.union(a_set, b_set)

    return accepted_edges