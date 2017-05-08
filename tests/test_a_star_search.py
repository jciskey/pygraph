"""Provides unit tests to verify that the A* search algorithm is functioning correctly."""

import unittest

from ..pygraph import UndirectedGraph, a_star_search
from . import utility_functions
from ..pygraph.exceptions import NonexistentNodeError


class AStarSearchTest(unittest.TestCase):
    def test_a_star_search_with_invalid_nodes(self):
        """Does the ''a_star_search'' function throw an error for invalid nodes?"""
        graph = UndirectedGraph()

        # --Test 1: Empty graph, both nodes invalid
        node_a = 1
        node_b = 2

        try:
            path = a_star_search(graph, node_a, node_b)
        except NonexistentNodeError:
            pass
        else:
            self.fail('a_star_search function accepts an invalid node id for an empty graph')

        # --Test 2: Single-node graph, node_b invalid
        node_a = graph.new_node()

        try:
            path = a_star_search(graph, node_a, node_b)
        except NonexistentNodeError:
            pass
        else:
            self.fail('a_star_search function accepts an invalid node id {}'.format(node_b))

        # --Test 3: Single-node graph, node_a invalid
        node_b = graph.new_node()
        graph.delete_node(node_a)

        try:
            path = a_star_search(graph, node_a, node_b)
        except NonexistentNodeError:
            pass
        else:
            self.fail('a_star_search function accepts an invalid node id {}'.format(node_a))

        # --Test 4: Dual-node graph, both nodes valid
        node_a = graph.new_node()

        try:
            path = a_star_search(graph, node_a, node_b)
        except NonexistentNodeError:
            self.fail('a_star_search function throws an error with valid nodes')
        else:
            pass

    def test_a_star_search_with_single_path(self):
        """Does the ''a_star_search'' function return a valid path when there's only one possible path?"""
        graph = utility_functions.build_simple_test_graph()

        expected_path = [4, 1, 2, 5]
        path = a_star_search(graph, 4, 5)

        self.assertEqual(expected_path, path)

    def test_a_star_search_with_direct_connection(self):
        """Does the ''a_star_search'' function return the shortest path when there is a direct connection?"""
        graph = utility_functions.build_simple_test_graph()

        # Add an edge to the graph to directly connect 2 nodes, providing a shorter path between them
        graph.new_edge(4, 5)

        expected_path = [4, 5]
        path = a_star_search(graph, 4, 5)

        self.assertEqual(expected_path, path)

    def test_a_star_search_with_path_choices(self):
        """Does the ''a_star_search'' function return the shortest path between multiple available paths?"""
        graph = utility_functions.build_simple_test_graph()

        # Add an edge to the graph to provide a shorter path between the start and goal nodes
        graph.new_edge(1, 5)

        expected_path = [4, 1, 5]
        path = a_star_search(graph, 4, 5)

        self.assertEqual(expected_path, path)

    def test_a_star_search_with_no_path(self):
        """Does the ''a_star_search'' function return an empty list when no path exists?"""
        graph = utility_functions.build_simple_test_graph()

        expected_path = []
        path = a_star_search(graph, 4, 3)

        self.assertEqual(expected_path, path)

    def test_a_star_search_with_square_graph_and_costs(self):
        """Does the ''a_star_search'' function return the proper path for a square graph with costs?"""
        graph = utility_functions.build_square_test_graph_with_costs()

        # --The edge from 1 to 4 costs 10, while the cost of the [1, 2, 3, 4] path is [2, 3, 1], which sums to 6
        expected_path = [1, 2, 3, 4]
        path = a_star_search(graph, 1, 4)

        self.assertEqual(expected_path, path)
