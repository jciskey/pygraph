"""
Implementing planarity testing as per "The Hopcroft-Tarjan Planarity Algorithm" by William Kocay
Location: http://www.combinatorialmath.ca/G&G/articles/planarity.pdf
"""

from collections import deque

from ..searching.depth_first_search import depth_first_search_with_parent_data


"""
In programming the Hopcroft-Tarjan algorithm one first begins with
the LowPtDFS in order to determine L1(v) and L2 (v). The adjacency lists
are then sorted by weight. Next, the BranchPtDFS can be executed in
order to establish the first node in Adj[u]. Then EmbedBranch is executed
in order to construct the lists LF and RF which determine the combina-
torial embedding of G. An alternative is to combine BranchPtDFS and
EmbedBranch into a single DFS, which is easy to do.
"""



def kocay_planarity_test(graph):
    """Determines whether a graph is planar."""

    adj = __calculate_adjacency_lists(graph)
    dfs_data = __get_dfs_data(graph)

    dfs_data['graph'] = graph

    L1, L2 = __low_point_dfs(dfs_data)
    #dfs_data['lowpoint_1_lookup'] = L1
    #dfs_data['lowpoint_2_lookup'] = L2

    #edge_weights = __calculate_edge_weights(dfs_data)
    #dfs_data['edge_weights'] = edge_weights

    #new_adj = __sort_adjacency_lists(adj, dfs_data)

    return False


def __low_point_dfs(dfs_data):
    """Calculates the L1 and L2 for each vertex."""
    L1, L2 = __get_all_lowpoints(dfs_data)
    return (L1, L2)


def __calculate_adjacency_lists(graph):
    """Builds an adjacency list representation for the graph, since we can't guarantee that the
        internal representation of the graph is stored that way."""
    adj = {}
    for node in graph.get_all_node_ids():
        neighbors = graph.neighbors(node)
        adj[node] = neighbors
    return adj


def __calculate_edge_weights(dfs_data):
    """Calculates the weight of each edge, for embedding-order sorting."""
    graph = dfs_data['graph']

    weights = {}
    for edge_id in graph.get_all_edge_id():
        edge_weight = __edge_weight(edge_id, dfs_data)
        weights[edge_id] = edge_weight

    return weights


def __sort_adjacency_lists(adjacency_lists, dfs_data):
    """Sorts the adjacency list representation by the edge weights."""
    new_adjacency_lists = {}

    edge_weights = dfs_data['edge_weights']
    edge_lookup = dfs_data['edge_lookup']

    def weight_lookup_fn(n):
        return node_weight_lookup[n]
    def frond_lookup_fn(n):
        return frond_lookup[n]

    for node_id, adj_list in adjacency_lists.items():
        node_weight_lookup = {}
        frond_lookup = {}
        for node_b in adj_list:
            edge_id = dfs_data['graph'].get_first_edge_id_by_node_ids(node_id, node_b)
            node_weight_lookup[node_b] = edge_weights[edge_id]
            frond_lookup[node_b] = 1 if edge_lookup[edge_id] == 'backedge' else 2

        # Fronds should be before branches if the weights are equal
        new_list = sorted(adj_list, key=frond_lookup_fn)

        # Sort by weights
        new_list.sort(key=weight_lookup_fn)

        # Add the new sorted list to the new adjacency list lookup table
        new_adjacency_lists[node_id] = new_list

    return new_adjacency_lists


def __branch_point_dfs():
    """Calculates the first node in the adjacency list for each node."""
    pass


def __embed_branch():
    """Builds the combinatorial embedding of the graph."""
    pass


# Helper functions -- these are not directly specified by the overall algorithm, they just calculate intermediate data

def __get_dfs_data(graph):
    """Internal function that calculates the depth-first search of the graph.
    Returns a dictionary with the following data:
        * 'ordering':        A dfs-ordering list of nodes
        * 'ordering_lookup': A lookup dict mapping nodes to dfs-ordering
        * 'node_lookup':     A lookup dict mapping dfs-ordering to nodes
        * 'edge_lookup':     A lookup dict mapping edges as tree-edges or back-edges
        * 'parent_lookup':   A lookup dict mapping nodes to their parent node
        * 'children_lookup': A lookup dict mapping nodes to their children
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

    dfs_data = {}
    dfs_data['ordering'] = ordering
    dfs_data['ordering_lookup'] = ordering_lookup
    dfs_data['node_lookup'] = node_lookup
    dfs_data['edge_lookup'] = edge_lookup
    dfs_data['parent_lookup'] = parent_lookup
    dfs_data['children_lookup'] = children_lookup

    return dfs_data


def __get_all_lowpoints(dfs_data):
    """Calculates the lowpoints for each node in a graph."""
    lowpoint_1_lookup = {}
    lowpoint_2_lookup = {}

    ordering = dfs_data['ordering']

    for node in ordering:
        low_1, low_2 = __get_lowpoints(node, dfs_data)
        lowpoint_1_lookup[node] = low_1
        lowpoint_2_lookup[node] = low_2

    return lowpoint_1_lookup, lowpoint_2_lookup


def __get_lowpoints(node, dfs_data):
    """Calculates the lowpoints for a single node in a graph."""

    ordering_lookup = dfs_data['ordering_lookup']

    #t_u = __descendant_neighbors(node, dfs_data)
    t_u = T(node, dfs_data)
    sorted_t_u = sorted(t_u, key=lambda a: ordering_lookup[a])
    lowpoint_1 = sorted_t_u[0]
    lowpoint_2 = sorted_t_u[1]

    return lowpoint_1, lowpoint_2


def __descendant_neighbors(node, dfs_data):
    """Calculates all the neighbors of a list of descendants."""
    list_of_descendants = S(node, dfs_data)

    neighbors_set = set()

    for d in list_of_descendants:
        nodes = A(d, dfs_data)
        for n in nodes:
            neighbors_set.add(n)

    return list(neighbors_set)


def __get_descendants(node, dfs_data):
    """Gets the descendants of a node."""
    list_of_descendants = []

    stack = deque()

    children_lookup = dfs_data['children_lookup']

    current_node = node
    children = children_lookup[current_node]
    dfs_current_node = D(current_node, dfs_data)
    for n in children:
        dfs_child = D(n, dfs_data)
        # Validate that the child node is actually a descendant and not an ancestor
        if dfs_child > dfs_current_node:
            stack.append(n)

    while len(stack) > 0:
        current_node = stack.pop()
        list_of_descendants.append(current_node)
        children = children_lookup[current_node]
        dfs_current_node = D(current_node, dfs_data)
        for n in children:
            dfs_child = D(n, dfs_data)
            # Validate that the child node is actually a descendant and not an ancestor
            if dfs_child > dfs_current_node:
                stack.append(n)

    return list_of_descendants


def __edge_weight(edge_id, dfs_data):
    """Calculates the edge weight used to sort edges."""
    graph = dfs_data['graph']
    edge_lookup = dfs_data['edge_lookup']

    edge = graph.get_edge(edge_id)
    u, v = edge['vertices']
    d_u = D(u, dfs_data)
    d_v = D(v, dfs_data)
    lp_1 = L1(v, dfs_data)
    d_lp_1 = D(lp_1, dfs_data)

    if edge_lookup[edge_id] == 'backedge' and d_v < d_u:
        return 2*d_v
    elif is_type_I_branch(u, v, dfs_data):
        return 2*d_lp_1
    elif is_type_II_branch(u, v, dfs_data):
        return 2*d_lp_1 + 1
    else:
        return 2*graph.num_nodes() + 1


def is_type_I_branch(u, v, dfs_data):
    """Determines whether a branch uv is a type I branch."""
    if u != a(v, dfs_data):
        return False
    if u == L2(v, dfs_data):
        return True
    return False


def is_type_II_branch(u, v, dfs_data):
    """Determines whether a branch uv is a type II branch."""
    if u != a(v, dfs_data):
        return False
    if u < L2(v, dfs_data):
        return True
    return False


# Wrapper functions -- used to keep the syntax roughly the same as that used in the paper

def A(u, dfs_data):
    """The adjacency function."""
    return dfs_data['graph'].neighbors(u)

def a(v, dfs_data):
    """The ancestor function."""
    return dfs_data['parent_lookup'][v]

def D(u, dfs_data):
    """The DFS-numbering function."""
    return dfs_data['ordering_lookup'][u]

def S(u, dfs_data):
    """The set of all descendants of u."""
    return __get_descendants(u, dfs_data)

def S_star(u, dfs_data):
    """The set of all descendants of u, with u added."""
    s_u = S(u, dfs_data)
    if u not in s_u:
        s_u.append(u)
    return s_u

def T(u, dfs_data):
    """T(u) consists of all vertices adjacent to u or any descendant of u."""
    return list(set([w for v in S_star(u, dfs_data) for w in A(v, dfs_data)]))

def L1(v, dfs_data):
    """The L1 lowpoint of the node."""
    return dfs_data['lowpoint_1_lookup'][v]

def L2(v, dfs_data):
    """The L2 lowpoint of the node."""
    return dfs_data['lowpoint_2_lookup'][v]

def wt(u, v, dfs_data):
    """The wt_u[v] function used in the paper."""
    # Determine the edge_id
    edge_id = dfs_data['graph'].get_first_edge_id_by_node_ids(u, v)
    # Pull the weight of that edge
    return dfs_data['edge_weights'][edge_id]

