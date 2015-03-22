"""Implementation of Breadth First Search."""

from collections import deque, defaultdict

def breadth_first_search(graph, root_node=None):
    """Searches through the tree in a breadth-first fashion.
        If root_node is None, an arbitrary node will be used as the root.
        If root_node is not None, it will be used as the root for the search tree.
        Returns a list of nodes, in the order that they were reached.
    """
    ordering = []
    queue = deque()
    visited = defaultdict(lambda: False)

    all_nodes = graph.get_all_node_ids()
    to_visit = set(all_nodes)
    if not all_nodes:
        return ordering

    if root_node is None:
        root_node = all_nodes[0]

    queue.appendleft(root_node)

    # We need to make sure we visit all the nodes, including disconnected ones
    while True:
        # BFS Main Loop
        while len(queue) > 0:
            current_node = queue.popleft()

            if not visited[current_node]:
                visited[current_node] = True
                ordering.append(current_node)
                to_visit.remove(current_node)

                for n in graph.neighbors(current_node):
                    if not visited[n]:
                        queue.appendleft(n)

        # New root node if we still have more nodes
        if len(to_visit) > 0:
            node = to_visit.pop()
            to_visit.add(node)
            queue.appendleft(node)
        else:
            break

    return ordering