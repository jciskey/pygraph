"""Provides unit testing of the DirectedGraph class in the main graphlib module."""

import unittest

from ..pygraph import DirectedGraph, NonexistentNodeError, NonexistentEdgeError
from . import utility_functions


class DGTest(unittest.TestCase):

    def test_correct_neighbors(self):
        """Does the ''neighbors'' method produce the proper list of neighbor nodes?"""
        # Test 1: Single node graph
        graph = utility_functions.build_single_node_graph(True)
        expected = []
        neighbors = graph.neighbors(1)
        self.assertEqual(expected, neighbors)

        # Test 2: 2-node graph
        graph = utility_functions.build_2_node_graph(True)
        test_list = [
            (1, [2]),
            (2, []),
        ]
        for node_id, expected_neighbors in test_list:
            neighbors = graph.neighbors(node_id)
            self.assertEqual(expected_neighbors, neighbors,
                             'Node {}: Expected {} !=  Actual {}'.format(node_id, expected_neighbors, neighbors))

        # Test 3: triangle graph
        graph = utility_functions.build_triangle_graph_with_costs(True)
        test_list = [
            (1, [2]),
            (2, [3]),
            (3, [1]),
        ]
        for node_id, expected_neighbors in test_list:
            neighbors = graph.neighbors(node_id)
            self.assertEqual(expected_neighbors, neighbors,
                             'Node {}: Expected {} !=  Actual {}'.format(node_id, expected_neighbors, neighbors))

        # Test 4: square graph
        graph = utility_functions.build_square_test_graph_with_costs(True)
        test_list = [
            (1, [2, 4]),
            (2, [3]),
            (3, [4]),
            (4, []),
        ]
        for node_id, expected_neighbors in test_list:
            neighbors = graph.neighbors(node_id)
            self.assertEqual(expected_neighbors, neighbors,
                             'Node {}: Expected {} !=  Actual {}'.format(node_id, expected_neighbors, neighbors))

    def test_new_edge_non_existent_node_errors(self):
        """Does the ''new_edge'' function throw errors when given non-existent nodes?"""
        graph = DirectedGraph()

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

        # Test both nodes existent
        node_a = graph.new_node()
        try:
            graph.new_edge(node_a, node_b)
        except NonexistentNodeError:
            self.fail('New edge throws error when given existing nodes')
        else:
            pass

    def test_neighbors_non_existent_node_error(self):
        """Does the ''neighbors'' function throw an error when given an non-existent node id?"""
        graph = DirectedGraph()

        node_id = 1

        try:
            graph.neighbors(node_id)
        except NonexistentNodeError:
            pass
        else:
            self.fail('neighbors function accepts non-existent node id {}'.format(node_id))

    def test_new_edge_return_value(self):
        """Does the ''new_edge'' method return an edge id?"""
        graph = DirectedGraph()

        node_a = graph.new_node()
        node_b = graph.new_node()

        edge_id = graph.new_edge(node_a, node_b)

        self.assertIsNotNone(edge_id)

    def test_delete_edge_with_bad_edge_raises_error(self):
        """Does the ''delete_edge_by_id'' method raise an error when given an invalid edge id?"""
        graph = DirectedGraph()

        edge_id = 1

        try:
            graph.delete_edge_by_id(edge_id)
        except NonexistentEdgeError:
            pass
        else:
            self.fail('Delete edge accepts an invalid edge id "{}"'.format(edge_id))

    def test_get_node_with_bad_node_raises_error(self):
        """Does the ''get_node'' method raise an error when given an invalid node id?"""
        graph = DirectedGraph()

        node_id = 1

        try:
            graph.get_node(node_id)
        except NonexistentNodeError:
            pass
        else:
            self.fail('Get node accepts an invalid node id "{}"'.format(node_id))

    def test_get_edge_with_bad_edge_raises_error(self):
        """Does the ''get_edge'' method raise an error when given an invalid edge id?"""
        graph = DirectedGraph()

        edge_id = 1

        try:
            graph.get_edge(edge_id)
        except NonexistentEdgeError:
            pass
        else:
            self.fail('Get edge accepts an invalid edge id "{}"'.format(edge_id))

    def test_adjacency(self):
        """Does the ''adjacent'' function correctly identify neighbor nodes in a directed graph?"""
        # Build the test graph
        graph = utility_functions.build_simple_test_graph(True)

        # Build the node pairs and test them
        pairs = [
            # (Node ID, Node ID, True/False)
            (1, 2, True),
            (1, 4, True),
            (6, 7, True),
            (2, 5, True),
            (2, 1, False),
            (4, 1, False),
            (7, 6, False),
            (1, 5, False),
            (2, 3, False),
            (3, 6, False),
        ]

        for node_a, node_b, expected in pairs:
            actual = graph.adjacent(node_a, node_b)
            self.assertEqual(actual, expected, 'node_a {}, node_b {}'.format(node_a, node_b))