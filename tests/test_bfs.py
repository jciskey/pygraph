"""Provides unit tests to verify that the Breadth First Search algorithm is functioning correctly."""

import unittest
from collections import defaultdict

from ..pygraph import UndirectedGraph, breadth_first_search
from . import utility_functions


class BreadthFirstSearchTest(unittest.TestCase):

    def test_bfs_with_empty_graph(self):
        """Does the ''breadth_first_search'' function return an empty list for an empty graph?"""
        graph = UndirectedGraph()

        expected = []
        ordering = breadth_first_search(graph)

        self.assertEqual(expected, ordering)

    def test_bfs_with_single_node(self):
        """Does the ''breadth_first_search'' function return a single node when given a trivial graph?"""
        graph = utility_functions.build_single_node_graph()

        expected = [1]
        ordering = breadth_first_search(graph)

        self.assertEqual(expected, ordering)

    def test_bfs_with_line_graph(self):
        """Does the ''breadth_first_search'' function return the proper path for a line-graph?"""
        graph = utility_functions.build_3_node_line_graph()

        expected = [1, 2, 3]
        ordering = breadth_first_search(graph, 1)

        self.assertEqual(expected, ordering)

    def test_bfs_with_connected_graph_contains_all_nodes(self):
        """Does the ''breadth_first_search'' function return all the nodes for a connected graph?"""
        graph = utility_functions.build_biconnected_test_graph()

        all_nodes = graph.get_all_node_ids()
        ordering = breadth_first_search(graph, 1)

        self.assertEqual(len(all_nodes), len(ordering))

        for n in all_nodes:
            self.assertIn(n, ordering)

    def test_bfs_with_disconnected_graph_contains_all_nodes(self):
        """Does the ''breadth_first_search'' function return all the nodes for a disconnected graph?"""
        graph = utility_functions.build_disconnected_test_graph()

        all_nodes = graph.get_all_node_ids()
        ordering = breadth_first_search(graph, 1)

        self.assertEqual(len(all_nodes), len(ordering))

        for n in all_nodes:
            self.assertIn(n, ordering)

