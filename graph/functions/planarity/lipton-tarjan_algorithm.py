
from collections import deque

from ..searching.depth_first_search import depth_first_search_with_parent_data

def __get_all_lowpoints(graph):
    """Calculates the lowpoints for each node in a graph."""
    lowpoint_1_lookup = {}
    lowpoint_2_lookup = {}

    ordering, ordering_lookup, node_lookup, edge_lookup, parent_lookup, children_lookup = __get_dfs_data(graph)
    for node in ordering:
        low_1, low_2 = __get_lowpoints(node, graph, ordering_lookup, children_lookup)
        lowpoint_1_lookup[node] = low_1
        lowpoint_2_lookup[node] = low_2

    return lowpoint_1_lookup, lowpoint_2_lookup


def __get_lowpoints(node, graph, ordering_lookup, children_lookup):
    t_u = __descendant_neighbors(node, graph, children_lookup)
    sorted_t_u = sorted(t_u, key=lambda a: ordering_lookup[a])
    lowpoint_1 = sorted_t_u[0]
    lowpoint_2 = sorted_t_u[1]

    return lowpoint_1, lowpoint_2


def __get_dfs_data(graph):
    """Internal function that calculates the depth-first search of the graph.
    Returns:
        * A dfs-ordering list of nodes
        * A lookup dict mapping nodes to dfs-ordering
        * A lookup dict mapping dfs-ordering to nodes
        * A lookup dict mapping edges as tree-edges or back-edges
        * A lookup dict mapping nodes to their parent node
        * A lookup dict mapping nodes to their children
    """
    ordering, parent_lookup, children_lookup = depth_first_search_with_parent_data(graph)
    ordering_lookup = dict(zip(ordering, range(1, len(ordering) + 1)))
    node_lookup = dict(zip(range(1, len(ordering) + 1), ordering))
    edge_lookup = {}

    for edge_id in graph.get_all_edge_ids():
        edge = graph.get_edge(edge_id)
        node_a, node_b = edge['vertices']
        parent_a = parent_lookup[node_a]
        parent_b = parent_lookup[node_b]
        if parent_a == node_b or parent_b == node_a:
            edge_lookup[edge_id] = 'tree-edge'
        else:
            edge_lookup[edge_id] = 'backedge'

    return ordering, ordering_lookup, node_lookup, edge_lookup, parent_lookup, children_lookup


def __get_descendants(node, children_lookup):
    """Gets the descendants of a node."""
    list_of_descendants = []

    stack = deque()

    current_node = node
    children = children_lookup[current_node]
    for n in children:
        stack.append(n)

    while len(stack) > 0:
        current_node = stack.pop()
        list_of_descendants.append(current_node)
        children = children_lookup[current_node]
        for n in children:
            stack.append(n)

    return list_of_descendants


def __descendant_neighbors(node, graph, children_lookup):
    """Calculates all the neighbors of a list of descendants."""
    list_of_descendants = __get_descendants(node, children_lookup)

    neighbors_set = set()

    for d in list_of_descendants:
        nodes = graph.neighbors(d)
        for n in nodes:
            neighbors_set.add(n)

    return list(neighbors_set)


def __get_cycle(graph, ordering, parent_lookup):
    """Gets the main cycle of the dfs tree."""
    root_node = ordering[0]
    for i in range(2, len(ordering)):
        current_node = ordering[i]
        if graph.adjacent(current_node, root_node):
            path = []
            while current_node != root_node:
                path.append(current_node)
                current_node = parent_lookup[current_node]
            path.append(root_node)
            path.reverse()
            return path


def __get_segments_from_node(node, graph):
    """Calculates the segments that can emanate from a particular node on the main cycle."""
    list_of_segments = []
    node_object = graph.get_node(node)
    for e in node_object['edges']:
        list_of_segments.append(e)
    return list_of_segments


def __get_segments_from_cycle(graph, cycle_path):
    """Calculates the segments that emanate from the main cycle."""
    list_of_segments = []
    # We work through the cycle in a bottom-up fashion
    for n in cycle_path[::-1]:
        segments = __get_segments_from_node(n, graph)
        if segments:
            list_of_segments.append(segments)

    return list_of_segments



def __edge_weight(edge_id, graph, ordering_lookup, parent_lookup, edge_lookup, lowpoint_1_lookup, lowpoint_2_lookup):
    """Calculates the edge weight used to sort edges."""
    edge = graph.get_edge(edge_id)
    u, v = edge['vertices']
    dfs_u = ordering_lookup[u]
    dfs_v = ordering_lookup[v]
    low_1 = lowpoint_1_lookup[v]
    low_2 = lowpoint_2_lookup[v]

    if edge_lookup[edge_id] == 'backedge' and dfs_v < dfs_u:
        return 2*dfs_v
    elif parent_lookup[v] == u and low_2 == u:
        return 2*ordering_lookup[low_1]
    elif parent_lookup[v] == u and low_2 < u:
        return 2*ordering_lookup[low_1] + 1
    else:
        return 2*graph.num_nodes() + 1