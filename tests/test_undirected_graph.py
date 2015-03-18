"""Provides unit testing of the DirectedGraph class in the main graphlib module."""

import unittest

from ..graph import UndirectedGraph
from . import utility_functions


class UDGTest(unittest.TestCase):

	def test_new_edge_return_value(self):
		"""Does the ''new_edge'' method return an edge id?"""
		graph = UndirectedGraph()

		graph.new_node()
		graph.new_node()

		edge_id = graph.new_edge(1,2)

		self.assertIsNotNone(edge_id)

	def test_correct_neighbors(self):
		"""Does the ''neighbors'' method produce the proper list of neighbor nodes in an undirected graph?"""
		#Build the test graph
		graph = utility_functions.build_simple_test_graph()

		#Build the pairs and test them
		pairs = [
			# (Node ID, List of Neighbors)
			(1, [2,4]),
			(2, [1,5]),
			(3, []),
			(4, [1]),
			(5, [2]),
			(6, [7]),
			(7, [6]),
		]

		for node_id, expected_neighbors in pairs:
			actual_neighbors = graph.neighbors(node_id)
			self.assertEqual(actual_neighbors, expected_neighbors) #, msg="\n".join(['{}'.format(graph.get_edge(edge_id)) for edge_id in graph.get_node(node_id)['edges']]))

	def test_adjacency(self):
		"""Does the ''adjacent'' function correctly identify neighbor nodes in an undirected graph?"""
		#Build the test graph
		graph = utility_functions.build_simple_test_graph()

		#Build the node pairs and test them
		pairs = [
			# (Node ID, Node ID, True/False)
			(1,2,True),
			(1,4,True),
			(6,7,True),
			(1,5,False),
			(2,3,False),
			(3,6,False),
		]

		for node_a, node_b, expected in pairs:
			actual = graph.adjacent(node_a,node_b)
			self.assertEqual(actual,expected)

	def test_existent_edge_cost(self):
		"""Does the ''edge_cost'' function return the appropriate cost for an edge that exists in an undirected graph?"""
		graph = utility_functions.build_simple_test_graph()

		#We currently don't use edge costs, so any existent edge should have a cost of 1
		nodes_with_edges = [
			(1,2),
			(1,4),
			(2,5),
			(6,7)
		]

		for node_a, node_b in nodes_with_edges:
			cost = graph.edge_cost(node_a, node_b)
			self.assertEqual(1, cost)

	def test_nonexistent_edge_cost(self):
		"""Does the ''edge_cost'' function return infinity for a nonexistent edge in an undirected graph?"""
		graph = utility_functions.build_simple_test_graph()

		nodes_without_edges = [
			(1,3), (1,5), (1,6), (1,7),
			(2,3), (2,4), (2,6), (2,7),
			(3,4), (3,5), (3,6), (3,7),
			(4,5), (4,6), (4,7),
			(5,6), (5,7)
		]

		for node_a, node_b in nodes_without_edges:
			cost = graph.edge_cost(node_a, node_b)
			self.assertEqual(float('inf'), cost)
