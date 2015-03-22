"""Implementation of Depth First Search."""

from collections import deque, defaultdict

def depth_first_search(graph, root_node=None):
    """Searches through the tree in a breadth-first fashion.
        If root_node is None, an arbitrary node will be used as the root.
        If root_node is not None, it will be used as the root for the search tree.
        Returns a list of nodes, in the order that they were reached.
    """
    ordering = []

    all_nodes = graph.get_all_node_ids()
    if not all_nodes:
        return ordering

    stack = deque()
    discovered = defaultdict(lambda: False)
    unvisited_nodes = set(all_nodes)

    if root_node is None:
        root_node = all_nodes[0]

    # --Initialize the stack, simulating the DFS call on the root node
    stack.appendleft(root_node)

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
                neighbors = graph.neighbors(u)
                for n in neighbors:
                    stack.appendleft(n)

        # While there are still nodes that need visiting, repopulate the stack
        if len(unvisited_nodes) > 0:
            u = unvisited_nodes.pop()
            stack.appendleft(u)
        else:
            break

    return ordering