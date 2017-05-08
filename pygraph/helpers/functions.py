"""Gathers together a collection of helper functions and classes that the library needs,
but end users won't care about."""

import copy

from ..classes import UndirectedGraph, DirectedGraph


# Graph Conversions

def make_subgraph(graph, vertices, edges):
    """Converts a subgraph given by a list of vertices and edges into a graph object."""
    # Copy the entire graph
    local_graph = copy.deepcopy(graph)

    # Remove all the edges that aren't in the list
    edges_to_delete = filter(lambda x: x not in edges, local_graph.get_all_edge_ids())
    for e in edges_to_delete:
        local_graph.delete_edge_by_id(e)

    # Remove all the vertices that aren't in the list
    nodes_to_delete = filter(lambda x: x not in vertices, local_graph.get_all_node_ids())
    for n in nodes_to_delete:
        local_graph.delete_node(n)

    return local_graph


def convert_graph_directed_to_undirected(dg):
    """Converts a directed graph into an undirected graph. Directed edges are made undirected."""

    udg = UndirectedGraph()

    # Copy the graph
    # --Copy nodes
    # --Copy edges
    udg.nodes = copy.deepcopy(dg.nodes)
    udg.edges = copy.deepcopy(dg.edges)
    udg.next_node_id = dg.next_node_id
    udg.next_edge_id = dg.next_edge_id

    # Convert the directed edges into undirected edges
    for edge_id in udg.get_all_edge_ids():
        edge = udg.get_edge(edge_id)
        target_node_id = edge['vertices'][1]
        target_node = udg.get_node(target_node_id)
        target_node['edges'].append(edge_id)

    return udg


def remove_duplicate_edges_directed(dg):
    """Removes duplicate edges from a directed graph."""
    # With directed edges, we can just hash the to and from node id tuples and if
    # a node happens to conflict with one that already exists, we delete it

    # --For aesthetic, we sort the edge ids so that lower edge ids are kept
    lookup = {}
    edges = sorted(dg.get_all_edge_ids())
    for edge_id in edges:
        e = dg.get_edge(edge_id)
        tpl = e['vertices']
        if tpl in lookup:
            dg.delete_edge_by_id(edge_id)
        else:
            lookup[tpl] = edge_id


def remove_duplicate_edges_undirected(udg):
    """Removes duplicate edges from an undirected graph."""
    # With undirected edges, we need to hash both combinations of the to-from node ids, since a-b and b-a are equivalent
    # --For aesthetic, we sort the edge ids so that lower edges ids are kept
    lookup = {}
    edges = sorted(udg.get_all_edge_ids())
    for edge_id in edges:
        e = udg.get_edge(edge_id)
        tpl_a = e['vertices']
        tpl_b = (tpl_a[1], tpl_a[0])
        if tpl_a in lookup or tpl_b in lookup:
            udg.delete_edge_by_id(edge_id)
        else:
            lookup[tpl_a] = edge_id
            lookup[tpl_b] = edge_id


def get_vertices_from_edge_list(graph, edge_list):
    """Transforms a list of edges into a list of the nodes those edges connect.
    Returns a list of nodes, or an empty list if given an empty list.
    """
    node_set = set()
    for edge_id in edge_list:
        edge = graph.get_edge(edge_id)
        a, b = edge['vertices']
        node_set.add(a)
        node_set.add(b)

    return list(node_set)


def get_subgraph_from_edge_list(graph, edge_list):
    """Transforms a list of edges into a subgraph."""
    node_list = get_vertices_from_edge_list(graph, edge_list)
    subgraph = make_subgraph(graph, node_list, edge_list)

    return subgraph


def merge_graphs(main_graph, addition_graph):
    """Merges an ''addition_graph'' into the ''main_graph''.
    Returns a tuple of dictionaries, mapping old node ids and edge ids to new ids.
    """

    node_mapping = {}
    edge_mapping = {}

    for node in addition_graph.get_all_node_objects():
        node_id = node['id']
        new_id = main_graph.new_node()
        node_mapping[node_id] = new_id

    for edge in addition_graph.get_all_edge_objects():
        edge_id = edge['id']
        old_vertex_a_id, old_vertex_b_id = edge['vertices']
        new_vertex_a_id = node_mapping[old_vertex_a_id]
        new_vertex_b_id = node_mapping[old_vertex_b_id]
        new_edge_id = main_graph.new_edge(new_vertex_a_id, new_vertex_b_id)
        edge_mapping[edge_id] = new_edge_id

    return node_mapping, edge_mapping


def create_graph_from_adjacency_matrix(adjacency_matrix):
    """Generates a graph from an adjacency matrix specification.
       Returns a tuple containing the graph and a list-mapping of node ids to matrix column indices.

       The graph will be an UndirectedGraph if the provided adjacency matrix is symmetric.
       The graph will be a DirectedGraph if the provided adjacency matrix is not symmetric.
       Ref: http://mathworld.wolfram.com/AdjacencyMatrix.html"""
    if is_adjacency_matrix_symmetric(adjacency_matrix):
        graph = UndirectedGraph()
    else:
        graph = DirectedGraph()

    node_column_mapping = []

    num_columns = len(adjacency_matrix)
    for _ in xrange(num_columns):
        node_id = graph.new_node()
        node_column_mapping.append(node_id)

    for j in xrange(num_columns):
        for i in xrange(num_columns):
            if adjacency_matrix[j][i]:
                jnode_id = node_column_mapping[j]
                inode_id = node_column_mapping[i]
                # Because of our adjacency matrix encoding, [j][i] in our code corresponds to [i][j] in a traditional matrix interpretation
                # Thus, we need to put an edge from node i to node j if [j][i] in our code is non-zero
                graph.new_edge(inode_id, jnode_id)

    return (graph, node_column_mapping)


def is_adjacency_matrix_symmetric(adjacency_matrix):
    """Determines if an adjacency matrix is symmetric.
       Ref: http://mathworld.wolfram.com/SymmetricMatrix.html"""
    # Verify that the matrix is square
    num_columns = len(adjacency_matrix)
    for column in adjacency_matrix:
        # In a square matrix, every row should be the same length as the number of columns
        if len(column) != num_columns:
            return False

    # Loop through the bottom half of the matrix and compare it to the top half
    # --We do the bottom half because of how we construct adjacency matrices
    max_i = 0
    for j in xrange(num_columns):
        for i in xrange(max_i):
            # If i == j, we can skip ahead so we don't compare with ourself
            if i == j:
                continue
            # Compare the value in the bottom half with the mirrored value in the top half
            # If they aren't the same, the matrix isn't symmetric
            if adjacency_matrix[j][i] != adjacency_matrix[i][j]:
                return False
        max_i += 1

    # If we reach this far without returning false, then we know that everything matched,
    # which makes this a symmetric matrix
    return True

