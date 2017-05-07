"""Provides unit tests to verify that the planarity testing algorithm is functioning correctly."""

import unittest

from ..graph import UndirectedGraph, is_planar, build_k5_graph, build_k33_graph, build_groetzch_graph, build_franklin_graph, build_chvatal_graph
from . import utility_functions


class IsPlanarTest(unittest.TestCase):
    def test_empty_graph_is_planar(self):
        """Does the ''is_planar'' function classify an empty graph as planar?"""
        graph = UndirectedGraph()

        expected = True
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_single_node_graph_is_planar(self):
        """Does the ''is_planar'' function classify a single-node graph as planar?"""
        graph = utility_functions.build_single_node_graph()

        expected = True
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_2_node_graph_is_planar(self):
        """Does the ''is_planar'' function classify a 2-node graph as planar?"""
        graph = utility_functions.build_2_node_graph()

        expected = True
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_triangle_graph_is_planar(self):
        """Does the ''is_planar'' function classify a triangle graph as planar?"""
        graph = utility_functions.build_triangle_graph()

        expected = True
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_simple_planar_graph(self):
        """Does the ''is_planar'' function correctly classify the simple test graph as planar?"""
        graph = utility_functions.build_simple_test_graph()

        expected = True
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_disconnected_triangle_graphs_is_planar(self):
        """Does the ''is_planar'' function correctly classify the disconnected graph
        composed of triangle graphs as planar?
        """
        graph = utility_functions.build_disconnected_test_graph()

        expected = True
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_tiny_ring_graph_is_planar(self):
        """Does the ''is_planar'' function correctly classify a tiny ring graph as planar?"""
        graph = utility_functions.build_ring_graph(4)

        expected = True
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_small_ring_graph_is_planar(self):
        """Does the ''is_planar'' function correctly classify a small ring graph as planar?"""
        graph = utility_functions.build_ring_graph(10)

        expected = True
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_large_ring_graph_is_planar(self):
        """Does the ''is_planar'' function correctly classify a large ring graph as planar?"""
        graph = utility_functions.build_ring_graph(100)

        expected = True
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_k5_graph_not_planar(self):
        """Does the ''is_planar'' function correctly classify the K5 graph as non-planar?"""
        graph = build_k5_graph()

        expected = False
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_k33_graph_not_planar(self):
        """Does the ''is_planar'' function correctly classify the K3,3 graph as non-planar?"""
        graph = build_k33_graph()

        expected = False
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_k5_subgraph_not_planar(self):
        """Does the ''is_planar'' function correctly classify a graph with a K5 subgraph as non-planar?"""
        graph = utility_functions.build_non_planar_test_graph_with_k5_subgraph()

        expected = False
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_disconnected_k5_subgraph_not_planar(self):
        """Does the ''is_planar'' function correctly classify a graph with a K5 subgraph as non-planar?"""
        graph = utility_functions.build_non_planar_disconnected_test_graph_with_k5_subgraph()

        expected = False
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_k33_subgraph_not_planar(self):
        """Does the ''is_planar'' function correctly classify a graph with a K3,3 subgraph as non-planar?"""
        graph = utility_functions.build_non_planar_test_graph_with_k33_subgraph()

        expected = False
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_petersons_graph_not_planar(self):
        """Does the ''is_planar'' function correctly classify Peterson's graph as non-planar?"""
        graph = utility_functions.build_petersons_graph()

        expected = False
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_groetzch_graph_not_planar(self):
        """Does the ''is_planar'' function correctly classify the Groetzch graph as non-planar?"""
        graph = build_groetzch_graph()

        expected = False
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_franklin_graph_not_planar(self):
        """Does the ''is_planar'' function correctly classify the Franklin graph as non-planar?"""
        graph = build_franklin_graph()

        expected = False
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

    def test_chvatal_graph_not_planar(self):
        """Does the ''is_planar'' function correctly classify the Chvatal graph as non-planar?"""
        graph = build_chvatal_graph()

        expected = False
        planarity = is_planar(graph)

        self.assertEqual(expected, planarity)

