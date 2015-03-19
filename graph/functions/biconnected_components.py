"""Implements functionality to find biconnected components."""

import copy
from collections import deque, defaultdict

from .connected_components import get_connected_components_as_subgraphs


def find_biconnected_components(graph, alter_in_place=False):
    """Finds all the biconnected components in a graph.
    Returns a list of lists, each containing the edges that form a biconnected component.
    Returns an empty list for an empty graph.
    """
    if alter_in_place:
        local_graph = graph
    else:
        local_graph = copy.deepcopy(graph)

    list_of_components = []

    # Run the algorithm on each of the connected components of the graph
    components = get_connected_components_as_subgraphs(local_graph)
    for component in components:
        # --Call the internal biconnnected components function to find
        # --the edge lists for this particular connected component
        edge_list = _internal_get_biconnected_components_edge_lists(component)
        list_of_components.extend(edge_list)

    return list_of_components


def find_articulation_vertices(graph, alter_in_place=False):
    """Finds all of the articulation vertices within a graph."""
    root = graph.get_all_node_ids()[0]


# Helper functions
def _internal_get_biconnected_components_edge_lists(graph):
    """Works on a single connected component to produce the edge lists of the biconnected components.
    Returns a list of lists, each containing the edges that combine to produce the connected component.
    Returns a single nested list with 1 edge if there is only 1 edge in the graph (a 2-node graph is a
    special case, generally considered to be a biconnected graph).
    Returns an empty list if there are no edges in the graph (i.e. if it's a single-node or empty graph).
    """
    list_of_components = []

    num_nodes = len(graph.get_all_node_ids())
    num_edges = len(graph.get_all_edge_ids())
    if num_nodes <= 2:
        if num_edges == 1:
            list_of_components.append(graph.get_all_edge_ids())
        return list_of_components

    dfs_count = 0
    edge_stack = deque()
    dfs_stack = deque()
    visited = defaultdict(lambda: False)
    parent = defaultdict(lambda: None)
    depth = {}
    low = {}
    preorder_processed = defaultdict(lambda: False)
    postorder_processed = defaultdict(lambda: False)

    # We're simulating a recursive DFS with an explicit stack, since Python has a really small function stack
    unvisited_nodes = set(graph.get_all_node_ids())
    while len(unvisited_nodes) > 0:
        # --Initialize the first stack frame, simulating the DFS call on the root node
        u = unvisited_nodes.pop()
        parent[u] = u
        stack_frame = {
            'u': u,
            'v': None,
            'remaining_children': graph.neighbors(u)
        }
        dfs_stack.appendleft(stack_frame)

        while len(dfs_stack) > 0:
            frame = dfs_stack.popleft()
            u = frame['u']
            v = frame['v']

            if not visited[u]:
                if u in unvisited_nodes:
                    unvisited_nodes.remove(u)
                visited[u] = True
                dfs_count += 1
                depth[u] = dfs_count
                low[u] = depth[u]
                v = frame['remaining_children'].pop()
                frame['v'] = v

            if v is None:
                # --u has no neighbor nodes
                continue

            if not preorder_processed[v]:
                # --This is the preorder processing, done for each neighbor node ''v'' of u
                node_v = graph.get_node(v)
                for edge_id in node_v['edges']:
                    edge = graph.get_edge(edge_id)
                    tpl_a = (u, v)
                    tpl_b = (v, u)
                    if tpl_a == edge['vertices'] or tpl_b == edge['vertices']:
                        edge_stack.appendleft(edge_id)
                        break
                parent[v] = u
                preorder_processed[v] = True
                # print 'preorder for {}'.format(v)
                dfs_stack.appendleft(frame)

                # --Simulate the recursion to call the DFS on v
                new_frame = {
                    'u': v,
                    'v': None,
                    'remaining_children': graph.neighbors(v)
                }
                dfs_stack.appendleft(new_frame)
                continue

            elif not postorder_processed[v] and u == parent[v]:
                # --This is the postorder processing, done for each neighbor node ''v'' of u
                if low[v] >= depth[u]:
                    component = output_component(graph, edge_stack, u, v)
                    if len(component) > 2:
                        # --You can't have a biconnected component with less than 3 edges
                        list_of_components.append(component)
                low[u] = min(low[u], low[v])
                postorder_processed[v] = True
                # print 'postorder for {}'.format(v)

            elif visited[v] and (parent[u] != v) and (depth[v] < depth[u]):
                # (u,v) is a backedge from u to its ancestor v
                node_v = graph.get_node(v)
                for edge_id in node_v['edges']:
                    edge = graph.get_edge(edge_id)
                    tpl_a = (u, v)
                    tpl_b = (v, u)
                    if tpl_a == edge['vertices'] or tpl_b == edge['vertices']:
                        edge_stack.appendleft(edge_id)
                        break
                low[u] = min(low[u], depth[v])

            if len(frame['remaining_children']) > 0:
                # --Continue onto the next neighbor node of u
                v = frame['remaining_children'].pop()
                frame['v'] = v
                dfs_stack.appendleft(frame)

    return list_of_components


def output_component(graph, edge_stack, u, v):
    """Helper function to pop edges off the stack and produce a list of them."""
    edge_list = []
    while len(edge_stack) > 0:
        edge_id = edge_stack.popleft()
        edge_list.append(edge_id)

        edge = graph.get_edge(edge_id)
        tpl_a = (u, v)
        tpl_b = (v, u)
        if tpl_a == edge['vertices'] or tpl_b == edge['vertices']:
            break

    return edge_list