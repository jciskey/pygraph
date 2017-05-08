"""Provides unit tests to verify that the spanning tree algorithms are functioning correctly."""

import unittest

from ..pygraph import UndirectedGraph, find_minimum_spanning_tree, find_minimum_spanning_forest, DisconnectedGraphError
from . import utility_functions


class MSTTest(unittest.TestCase):
    def test_mst_with_empty_graph(self):
        """Does the ''find_minimum_spanning_tree'' function return an empty list for an empty graph?"""
        graph = UndirectedGraph()

        expected = []
        mst = find_minimum_spanning_tree(graph)

        self.assertEqual(expected, mst)

    def test_mst_with_single_node_graph(self):
        """Does the ''find_minimum_spanning_tree'' function return an empty list for a single-node graph?"""
        graph = utility_functions.build_single_node_graph()

        expected = []
        mst = find_minimum_spanning_tree(graph)

        self.assertEqual(expected, mst)

    def test_mst_with_2_node_graph(self):
        """Does the ''find_minimum_spanning_tree'' function return a single edge for a 2-node graph?"""
        graph = utility_functions.build_2_node_graph()

        expected = [1]
        mst = find_minimum_spanning_tree(graph)

    def test_mst_with_triangle_graph(self):
        """Does the ''find_minimum_spanning_tree'' function return the
        proper 2 edges for a triangle graph with costs?
        """
        graph = utility_functions.build_triangle_graph_with_costs()

        expected = [1, 2]
        mst = find_minimum_spanning_tree(graph)
        mst.sort()

        self.assertEqual(expected, mst)

    def test_mst_with_costing_square_graph(self):
        """Does the ''find_minimum_spanning_tree'' function return the proper 3 edges for a square graph with costs?"""
        graph = utility_functions.build_square_test_graph_with_costs()

        expected = [1, 3, 4]
        mst = find_minimum_spanning_tree(graph)
        mst.sort()

        self.assertEqual(expected, mst)

    def test_mst_with_unique_mst(self):
        """Does the ''find_minimum_spanning_tree'' function return the unique mst for a particular graph?"""
        graph = utility_functions.build_complicated_test_graph_with_one_mst()

        expected = [1, 3, 6, 10, 11, 12]
        mst = find_minimum_spanning_tree(graph)
        mst.sort()

        self.assertEqual(expected, mst)

    def test_mst_with_disconnected_subgraphs(self):
        """Does the ''find_minimum_spanning_tree'' function throw an error for a disconnected graph?"""
        graph = utility_functions.build_disconnected_test_graph()

        try:
            find_minimum_spanning_tree(graph)
        except DisconnectedGraphError:
            pass
        else:
            self.fail('find_minimum_spanning_tree function accepts a disconnected graph without error')

    def test_msf_with_disconnected_subgraphs(self):
        """Does the ''find_minimum_spanning_forest'' function return multiple msts for a disconnected graph?"""
        graph = utility_functions.build_disconnected_test_graph()

        expected_length = 3
        mst = find_minimum_spanning_forest(graph)

        self.assertEqual(expected_length, len(mst))