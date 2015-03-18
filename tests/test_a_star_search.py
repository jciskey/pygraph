"""Provides unit tests to verify that the A* search algorithm is functioning correctly."""

import unittest

from ..graph import a_star_search
from . import utility_functions

class AStarSearchTest(unittest.TestCase):

	def test_a_star_search_with_single_path(self):
		"""Does the ''a_star_search'' function return a valid path when there's only one possible path?"""
		graph = utility_functions.build_simple_test_graph()

		path = a_star_search(graph, 4, 5)

		expected_path = [4,1,2,5]

		self.assertEqual(expected_path, path)

	def test_a_star_search_with_direct_connection(self):
		"""Does the ''a_star_search'' function return the shortest path when there is a direct connection?"""
		graph = utility_functions.build_simple_test_graph()

		#Add an edge to the graph to directly connect 2 nodes, providing a shorter path between them
		graph.new_edge(4,5)

		path = a_star_search(graph, 4, 5)

		expected_path = [4,5]

		self.assertEqual(expected_path, path)

	def test_a_star_search_with_path_choices(self):
		"""Does the ''a_star_search'' function return the shortest path between multiple available paths?"""
		graph = utility_functions.build_simple_test_graph()

		#Add an edge to the graph to provide a shorter path between the start and goal nodes
		graph.new_edge(1,5)

		path = a_star_search(graph, 4, 5)

		expected_path = [4,1,5]

		self.assertEqual(expected_path, path)

	def test_a_star_search_with_no_path(self):
		"""Does the ''a_star_search'' function return an empty list when no path exists?"""
		graph = utility_functions.build_simple_test_graph()

		path = a_star_search(graph, 4, 3)

		expected_path = []

		self.assertEqual(expected_path, path)
