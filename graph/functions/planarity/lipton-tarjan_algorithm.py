

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

