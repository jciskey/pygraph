"""Provides unit tests to verify that the Breadth First Search algorithm is functioning correctly."""

import unittest
from collections import defaultdict

from ..pygraph import UndirectedGraph, depth_first_search, get_connected_components
from . import utility_functions


class DepthFirstSearchTest(unittest.TestCase):

    def test_dfs_with_empty_graph(self):
        """Does the ''depth_first_search'' function return an empty list for an empty graph?"""
        graph = UndirectedGraph()

        expected = []
        ordering = depth_first_search(graph)

        self.assertEqual(expected, ordering)

    def test_dfs_with_single_node(self):
        """Does the ''depth_first_search'' function return a single node when given a trivial graph?"""
        graph = utility_functions.build_single_node_graph()

        expected = [1]
        ordering = depth_first_search(graph)

        self.assertEqual(expected, ordering)

    def test_dfs_with_line_graph(self):
        """Does the ''depth_first_search'' function return the proper path for a line-graph?"""
        graph = utility_functions.build_3_node_line_graph()

        expected = [1, 2, 3]
        ordering = depth_first_search(graph, 1)

        self.assertEqual(expected, ordering)

    def test_dfs_depth_ordering(self):
        """Does the ''depth_first_search'' function return nodes in a proper ordering?"""
        graph = utility_functions.build_biconnected_test_graph()

        ordering = depth_first_search(graph, 1)
        node_lookup_by_index = dict(zip(range(1, len(ordering) + 1), ordering))
        items_sorted_by_dfs_index = zip(ordering, range(1, len(ordering) + 1))
        # index_lookup_by_node = dict(items_sorted_by_dfs_index)

        visited_by_node = defaultdict(lambda: False)

        connected_components = get_connected_components(graph)

        # If a node and its dfs-list successor are in the same connected component, and the non-successor node has
        # unvisited neighbors, then the successor must be one of those neighbors

        def in_same_component(node_a, node_b):
            for component in connected_components:
                if node_a in component:
                    return node_b in component
            return False

        for node_id, dfs_index in items_sorted_by_dfs_index[:-1]:
            visited_by_node[node_id] = True
            successor_node_id = node_lookup_by_index[dfs_index+1]
            if in_same_component(node_id, successor_node_id):
                neighbor_nodes = graph.neighbors(node_id)
                has_unvisited_neighbors = any(map(lambda n: not visited_by_node[n], neighbor_nodes))
                if has_unvisited_neighbors:
                    self.assertIn(successor_node_id, neighbor_nodes)

    def test_dfs_with_connected_graph_contains_all_nodes(self):
        """Does the ''depth_first_search'' function return all the nodes for a connected graph?"""
        graph = utility_functions.build_biconnected_test_graph()

        all_nodes = graph.get_all_node_ids()
        ordering = depth_first_search(graph, 1)

        self.assertEqual(len(all_nodes), len(ordering))

        for n in all_nodes:
            self.assertIn(n, ordering)

    def test_dfs_with_disconnected_graph_contains_all_nodes(self):
        """Does the ''depth_first_search'' function return all the nodes for a disconnected graph?"""
        graph = utility_functions.build_disconnected_test_graph()

        all_nodes = graph.get_all_node_ids()
        ordering = depth_first_search(graph, 1)

        self.assertEqual(len(all_nodes), len(ordering))

        for n in all_nodes:
            self.assertIn(n, ordering)

