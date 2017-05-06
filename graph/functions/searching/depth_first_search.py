"""Implementation of Depth First Search."""

from collections import deque, defaultdict

def depth_first_search(graph, root_node=None):
    """Searches through the tree in a breadth-first fashion.
        If root_node is None, an arbitrary node will be used as the root.
        If root_node is not None, it will be used as the root for the search tree.
        Returns a list of nodes, in the order that they were reached.
    """
    ordering, parent_lookup, children_lookup = depth_first_search_with_parent_data(graph, root_node)
    return ordering


def depth_first_search_with_parent_data(graph, root_node = None, adjacency_lists = None):
    """Performs a depth-first search with visiting order of nodes determined by provided adjacency lists,
     and also returns a parent lookup dict and a children lookup dict."""
    ordering = []
    parent_lookup = {}
    children_lookup = defaultdict(lambda: [])

    all_nodes = graph.get_all_node_ids()
    if not all_nodes:
        return ordering, parent_lookup, children_lookup

    stack = deque()
    discovered = defaultdict(lambda: False)
    unvisited_nodes = set(all_nodes)

    if root_node is None:
        root_node = all_nodes[0]

    if adjacency_lists is None:
        adj = lambda v: graph.neighbors(v)
    else:
        adj = lambda v: adjacency_lists[v]

    # --Initialize the stack, simulating the DFS call on the root node
    stack.appendleft(root_node)
    parent_lookup[root_node] = root_node

    # We're using a non-recursive implementation of DFS, since Python isn't great for deep recursion
    while True:
        # Main DFS Loop
        while len(stack) > 0:
            u = stack.popleft()

            if not discovered[u]:
                discovered[u] = True
                if u in unvisited_nodes:
                    unvisited_nodes.remove(u)
                ordering.append(u)
                neighbors = adj(u)
                # When adding the new nodes to the stack, we want to add them in reverse order so that
                # the order the nodes are visited is the same as with a recursive DFS implementation
                for n in neighbors[::-1]:
                    if discovered[n]:
                        # If the node already exists in the discovered nodes list
                        # we don't want to re-add it to the stack
                        continue
                    stack.appendleft(n)
                    parent_lookup[n] = u
                    children_lookup[u].append(n)

        # While there are still nodes that need visiting, repopulate the stack
        if len(unvisited_nodes) > 0:
            u = unvisited_nodes.pop()
            stack.appendleft(u)
        else:
            break

    return ordering, parent_lookup, children_lookup