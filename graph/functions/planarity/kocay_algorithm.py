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

    # We first have to calculate the DFS-tree of the graph, so we can calculate the edge weights to determine
    # the order of embedding of the branches
    adj = __calculate_adjacency_lists(graph)
    dfs_data = __setup_dfs_data(graph, adj)

    # Now that we have enough information to sort the edges, we should do so and then recalculate the DFS tree
    adj = __sort_adjacency_lists(dfs_data)
    dfs_data = __setup_dfs_data(graph, adj)

    # We now have the information we need to calculate the branch points
    b_u_lookup =__calculate_bu_dfs(dfs_data)
    dfs_data['b_u_lookup'] = b_u_lookup

    return False

def __setup_dfs_data(graph, adj):
    """Sets up the dfs_data object, for consistency."""
    dfs_data = __get_dfs_data(graph)

    dfs_data['graph'] = graph
    dfs_data['adj'] = adj

    L1, L2 = __low_point_dfs(dfs_data)
    dfs_data['lowpoint_1_lookup'] = L1
    dfs_data['lowpoint_2_lookup'] = L2

    edge_weights = __calculate_edge_weights(dfs_data)
    dfs_data['edge_weights'] = edge_weights

    return dfs_data


def __low_point_dfs(dfs_data):
    """Calculates the L1 and L2 for each vertex."""
    L1, L2 = __get_all_lowpoints(dfs_data)
    return (L1, L2)


def __calculate_edge_weights(dfs_data):
    """Calculates the weight of each edge, for embedding-order sorting."""
    graph = dfs_data['graph']

    weights = {}
    for edge_id in graph.get_all_edge_ids():
        edge_weight = __edge_weight(edge_id, dfs_data)
        weights[edge_id] = edge_weight

    return weights


def __sort_adjacency_lists(dfs_data):
    """Sorts the adjacency list representation by the edge weights."""
    new_adjacency_lists = {}

    adjacency_lists = dfs_data['adj']
    edge_weights = dfs_data['edge_weights']
    edge_lookup = dfs_data['edge_lookup']

    for node_id, adj_list in adjacency_lists.items():
        node_weight_lookup = {}
        frond_lookup = {}
        for node_b in adj_list:
            edge_id = dfs_data['graph'].get_first_edge_id_by_node_ids(node_id, node_b)
            node_weight_lookup[node_b] = edge_weights[edge_id]
            frond_lookup[node_b] = 1 if edge_lookup[edge_id] == 'backedge' else 2

        # Fronds should be before branches if the weights are equal
        new_list = sorted(adj_list, key=lambda n: frond_lookup[n])

        # Sort by weights
        new_list.sort(key=lambda n: node_weight_lookup[n])

        # Add the new sorted list to the new adjacency list lookup table
        new_adjacency_lists[node_id] = new_list

    return new_adjacency_lists


def __branch_point_dfs(dfs_data):
    """DFS that calculates the b(u) and N(u) lookups, and also reorders the adjacency lists."""
    u = dfs_data['ordering'][0]
    large_n = {}
    large_n[u] = 0
    stem = {}
    stem[u] = u
    b = {}
    b[u] = 0
    __branch_point_dfs_recursive(u, large_n, b, stem, dfs_data)
    dfs_data['N_u_lookup'] = large_n
    dfs_data['b_u_lookup'] = b
    return


def __branch_point_dfs_recursive(u, large_n, b, stem, dfs_data):
    """A recursive implementation of the BranchPtDFS function, as defined on page 14 of the paper."""
    v = dfs_data['adj'][u][0]
    large_w = wt(u, v, dfs_data)
    if large_w % 2 == 0:
        large_w += 1
    v_I = 0
    v_II = 0
    for v in [v for v in dfs_data['adj'][u] if wt(u, v, dfs_data) <= large_w]:
        if a(v, dfs_data) == u:
            large_n[v] = 0
            if wt(u, v, dfs_data) % 2 == 0:
                v_I = v
            else:
                b_u = b(u, dfs_data)
                l2_v = L2(v)
                if l2_v < b_u:
                    large_n[v] = 1
                elif b_u != 1:
                    x = stem[l2_v]
                    if large_n[x] != 0:
                        large_n[v] = large_n[x] + 1
                    elif dfs_data['graph'].adjacent(u, L1(v, dfs_data)):
                        large_n[v] = 2
                    else:
                        large_n[v] = large_n[u]
                if large_n[v] % 2 == 0:
                    v_II = v
                    break # Goto 1
    if v_II != 0:
        # Move v_II to head of Adj[u]
        dfs_data['adj'][u].remove(v_II)
        dfs_data['adj'][u].insert(0, v_II)
    elif v_I != 0:
        # Move v_I to head of Adj[u]
        dfs_data['adj'][u].remove(v_I)
        dfs_data['adj'][u].insert(0, v_I)
    first_time = True
    for v in dfs_data['adj'][u]:
        if a(v, dfs_data) == u:
            b[v] = u
            if first_time:
                b[v] = b[u]
            elif wt(u, v, dfs_data) % 2 == 0:
                large_n[v] = 0
            else:
                large_n[v] = 1
            stem[u] = v
            __branch_point_dfs_recursive(v, large_n, b, stem, dfs_data)
        first_time = False
    return


def __embed_branch(dfs_data):
    """Builds the combinatorial embedding of the graph."""
    u = dfs_data['ordering'][0]
    nonplanar = True
    LF = deque()
    RF = deque()
    __embed_branch_recursive(u, nonplanar, LF, RF, dfs_data)


def __embed_branch_recursive(u, nonplanar, LF, RF, dfs_data):
    """A recursive implementation of the EmbedBranch function, as defined on page 8 of the paper."""
    for v in dfs_data['adj'][u]:
        nonplanar = True
        if a(v, dfs_data) == u:
            if b(v, dfs_data) == u:
                if not __can_embed(v, LF, RF, dfs_data):
                    return
                buv = B(u, v, dfs_data)
                __insert_buv(buv, LF, RF, dfs_data)
            __embed_branch_recursive(v, nonplanar, LF, RF, dfs_data)
            if nonplanar:
                return
        elif is_frond(v, u, dfs_data):
            successful = __embed_frond(u, v, LF, RF, dfs_data)
            if not successful:
                return
    nonplanar = False
    return



# Helper functions -- these are not directly specified by the overall algorithm, they just calculate intermediate data

def __get_dfs_data(graph, adj=None):
    """Internal function that calculates the depth-first search of the graph.
    Returns a dictionary with the following data:
        * 'ordering':        A dfs-ordering list of nodes
        * 'ordering_lookup': A lookup dict mapping nodes to dfs-ordering
        * 'node_lookup':     A lookup dict mapping dfs-ordering to nodes
        * 'edge_lookup':     A lookup dict mapping edges as tree-edges or back-edges
        * 'parent_lookup':   A lookup dict mapping nodes to their parent node
        * 'children_lookup': A lookup dict mapping nodes to their children
    """
    ordering, parent_lookup, children_lookup = depth_first_search_with_parent_data(graph, adjacency_lists=adj)
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


def __calculate_adjacency_lists(graph):
    """Builds an adjacency list representation for the graph, since we can't guarantee that the
        internal representation of the graph is stored that way."""
    adj = {}
    for node in graph.get_all_node_ids():
        neighbors = graph.neighbors(node)
        adj[node] = neighbors
    return adj


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

    t_u = T(node, dfs_data)
    sorted_t_u = sorted(t_u, key=lambda a: ordering_lookup[a])
    lowpoint_1 = sorted_t_u[0]
    lowpoint_2 = sorted_t_u[1]

    return lowpoint_1, lowpoint_2


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


def __calculate_bu_dfs(dfs_data):
    """Calculates the b(u) lookup table."""
    u = dfs_data['ordering'][0]
    b = {}
    b[u] = D(u, dfs_data)
    __calculate_bu_dfs_recursively(u, b, dfs_data)
    return b


def __calculate_bu_dfs_recursively(u, b, dfs_data):
    """Calculates the b(u) lookup table with a recursive DFS."""
    first_time = True
    for v in dfs_data['adj'][u]:
        if a(v, dfs_data) == u:
            if first_time:
                b[v] = b[u]
            else:
                b[v] = D(u, dfs_data)
            __calculate_bu_dfs_recursively(v, b, dfs_data)
        first_time = False


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


def is_leaf(v, dfs_data):
    """Determines if v is a leaf (has no descendants)."""
    return True if S(v, dfs_data) else False


def is_frond(u, v, dfs_data):
    """Determines if the edge uv is a frond ("backedge")."""
    d_u = D(u, dfs_data)
    d_v = D(v, dfs_data)
    edge_id = dfs_data['graph'].get_first_edge_id_by_node_ids(u, v)
    return True if dfs_data['edge_lookup'][edge_id] == 'backedge' and d_v < d_u else False


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


# Wrapper functions -- used to keep the syntax roughly the same as that used in the paper

def A(u, dfs_data):
    """The adjacency function."""
    return dfs_data['adj'][u]


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


def B(u, v, dfs_data):
    """The branch at u containing v is the set of all edges incident on v or any descendant of v, if a(v) == u."""
    """Bu(v) = {wx | w is in S*(v)}"""
    if a(v, dfs_data) != u:
        return None

    return list(set([edge_id for w in S_star(v, dfs_data) for edge_id in dfs_data['graph'].get_node(w)['edges']]))


def stem(u, v, dfs_data):
    """The stem of Bu(v) is the edge uv in Bu(v)."""
    #return dfs_data['graph'].get_first_edge_id_by_node_ids(u, v)
    uv_edges = dfs_data['graph'].get_edge_ids_by_node_ids(u, v)
    buv_edges = B(u, v, dfs_data)
    for edge_id in uv_edges:
        if edge_id in buv_edges:
            return edge_id
    return None # We should never, ever get here


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


def L(dfs_data):
    """L(T) contains leaves and branch points for the DFS-tree T."""
    """L(T) = {v | the first w in Adj[v] corresponds to a frond vw}."""
    node_set = set()
    for v, adj in dfs_data['adj'].items():
        w = adj[0]
        if is_frond(v, w, dfs_data):
            node_set.add(v)
    return list(node_set)


def b(u, dfs_data):
    """The b(u) function used in the paper."""
    return dfs_data['b_u_lookup'][u]


def N(u, dfs_data):
    """The N(u) function used in the paper."""
    return dfs_data['N_u_lookup'][u]


def N_prime(u, dfs_data):
    """The N'(u) function used in the paper."""
    return dfs_data['N_prime_u_lookup'][u]