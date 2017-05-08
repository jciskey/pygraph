"""Provides unit testing of the UndirectedGraph class in the main graphlib module."""

import unittest

from ..pygraph import UndirectedGraph, NonexistentNodeError, NonexistentEdgeError
from . import utility_functions


class UDGTest(unittest.TestCase):
    def test_new_edge_with_bad_node_raises_error(self):
        """Does the ''new_edge'' method raise an error with invalid node ids?"""
        graph = UndirectedGraph()

        node_a = 1
        node_b = 2

        # Test both nonexistent
        try:
            graph.new_edge(node_a, node_b)
        except NonexistentNodeError:
            pass
        else:
            self.fail('New edge accepts invalid node ids "{}", "{}"'.format(node_a, node_b))

        # Test node_b nonexistent
        node_a = graph.new_node()
        try:
            graph.new_edge(node_a, node_b)
        except NonexistentNodeError:
            pass
        else:
            self.fail('New edge accepts an invalid node id "{}"'.format(node_b))

        # Test node_a nonexistent
        node_b = graph.new_node()
        graph.delete_node(node_a)
        try:
            graph.new_edge(node_a, node_b)
        except NonexistentNodeError:
            pass
        else:
            self.fail('New edge accepts an invalid node id "{}"'.format(node_a))

        # Test both nodes existant
        node_a = graph.new_node()
        try:
            graph.new_edge(node_a, node_b)
        except NonexistentNodeError:
            self.fail('New edge throws error when given existing nodes')
        else:
            pass

    def test_new_edge_return_value(self):
        """Does the ''new_edge'' method return an edge id?"""
        graph = UndirectedGraph()

        node_a = graph.new_node()
        node_b = graph.new_node()

        edge_id = graph.new_edge(node_a, node_b)

        self.assertIsNotNone(edge_id)

    def test_delete_edge_with_bad_edge_raises_error(self):
        """Does the ''delete_edge_by_id'' method raise an error when given an invalid edge id?"""
        graph = UndirectedGraph()

        edge_id = 1

        try:
            graph.delete_edge_by_id(edge_id)
        except NonexistentEdgeError:
            pass
        else:
            self.fail('Delete edge accepts an invalid edge id "{}"'.format(edge_id))

    def test_get_node_with_bad_node_raises_error(self):
        """Does the ''get_node'' method raise an error when given an invalid node id?"""
        graph = UndirectedGraph()

        node_id = 1

        try:
            graph.get_node(node_id)
        except NonexistentNodeError:
            pass
        else:
            self.fail('Get node accepts an invalid node id "{}"'.format(node_id))

    def test_get_edge_with_bad_edge_raises_error(self):
        """Does the ''get_edge'' method raise an error when given an invalid edge id?"""
        graph = UndirectedGraph()

        edge_id = 1

        try:
            graph.get_edge(edge_id)
        except NonexistentEdgeError:
            pass
        else:
            self.fail('Get edge accepts an invalid edge id "{}"'.format(edge_id))

    def test_correct_neighbors(self):
        """Does the ''neighbors'' method produce the proper list of neighbor nodes in an undirected graph?"""
        # Build the test graph
        graph = utility_functions.build_simple_test_graph()

        # Build the pairs and test them
        pairs = [
            # (Node ID, List of Neighbors)
            (1, [2, 4]),
            (2, [1, 5]),
            (3, []),
            (4, [1]),
            (5, [2]),
            (6, [7]),
            (7, [6]),
        ]

        for node_id, expected_neighbors in pairs:
            actual_neighbors = graph.neighbors(node_id)
            self.assertEqual(actual_neighbors,
                             expected_neighbors)

    def test_adjacency(self):
        """Does the ''adjacent'' function correctly identify neighbor nodes in an undirected graph?"""
        # Build the test graph
        graph = utility_functions.build_simple_test_graph()

        # Build the node pairs and test them
        pairs = [
            # (Node ID, Node ID, True/False)
            (1, 2, True),
            (1, 4, True),
            (6, 7, True),
            (1, 5, False),
            (2, 3, False),
            (3, 6, False),
        ]

        for node_a, node_b, expected in pairs:
            actual = graph.adjacent(node_a, node_b)
            self.assertEqual(actual, expected)
            actual = graph.adjacent(node_b, node_a)
            self.assertEqual(actual, expected)

    def test_existent_edge_cost(self):
        """Does the ''edge_cost'' function return the appropriate cost for an edge that
        exists in an undirected graph?"""
        graph = utility_functions.build_simple_test_graph()

        # Edges default to cost of 1
        nodes_with_edges = [
            (1, 2),
            (1, 4),
            (2, 5),
            (6, 7)
        ]

        for node_a, node_b in nodes_with_edges:
            cost = graph.edge_cost(node_a, node_b)
            self.assertEqual(1, cost)

    def test_nonexistent_edge_cost(self):
        """Does the ''edge_cost'' function return infinity for a nonexistent edge in an undirected graph?"""
        graph = utility_functions.build_simple_test_graph()

        nodes_without_edges = [
            (1, 3), (1, 5), (1, 6), (1, 7),
            (2, 3), (2, 4), (2, 6), (2, 7),
            (3, 4), (3, 5), (3, 6), (3, 7),
            (4, 5), (4, 6), (4, 7),
            (5, 6), (5, 7)
        ]

        for node_a, node_b in nodes_without_edges:
            cost = graph.edge_cost(node_a, node_b)
            self.assertEqual(float('inf'), cost)
