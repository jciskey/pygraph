"""Implements A* Search functionality."""

from ...helpers import PriorityQueue
from ...exceptions import NonexistentNodeError

def a_star_search(graph, start, goal):
    """Runs an A* search on the specified graph to find a path from the ''start'' node to the ''goal'' node.
    Returns a list of nodes specifying a minimal path between the two nodes.
    If no path exists (disconnected components), returns an empty list.
    """
    all_nodes = graph.get_all_node_ids()
    if start not in all_nodes:
        raise NonexistentNodeError(start)
    if goal not in all_nodes:
        raise NonexistentNodeError(goal)

    came_from, cost_so_far, goal_reached = _a_star_search_internal(graph, start, goal)
    if goal_reached:
        path = reconstruct_path(came_from, start, goal)
        path.reverse()
        return path
    else:
        return []


# A* Search Helpers
def heuristic(a, b):
    return 1


def _a_star_search_internal(graph, start, goal):
    """Performs an A* search, returning information about whether the goal node was reached
    and path cost information that can be used to reconstruct the path.
    """
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}
    goal_reached = False

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            goal_reached = True
            break

        for next_node in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.edge_cost(current, next_node)
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(goal, next_node)
                frontier.put(next_node, priority)
                came_from[next_node] = current

    return came_from, cost_so_far, goal_reached


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    return path
