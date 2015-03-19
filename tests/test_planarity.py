"""Provides unit tests to verify that the planarity testing algorithm is functioning correctly."""

import unittest

from ..graph import is_planar
from . import utility_functions


class IsPlanarTest(unittest.TestCase):
    def test_planar_graph(self):
        """Does the ''is_planar'' function correctly classify the simple test graph as planar?"""
        self.fail('Not implemented')

    def test_k5_graph_not_planar(self):
        """Does the ''is_planar'' function correctly classify the K5 graph as non-planar?"""
        self.fail('Not implemented')

    def test_k33_graph_not_planar(self):
        """Does the ''is_planar'' function correctly classify the K3,3 graph as non-planar?"""
        self.fail('Not implemented')

    def test_k5_subgraph_not_planar(self):
        """Does the ''is_planar'' function correctly classify a graph with a K5 subgraph as non-planar?"""
        self.fail('Not implemented')

    def test_k33_subgraph_not_planar(self):
        """Does the ''is_planar'' function correctly classify a graph with a K3,3 subgraph as non-planar?"""
        self.fail('Not implemented')