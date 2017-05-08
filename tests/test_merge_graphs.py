"""Provides unit tests to verify that the graph merging algorithm is functioning correctly."""

import unittest
import copy

from ..pygraph import UndirectedGraph, merge_graphs, build_triangle_graph
from . import utility_functions


class MergeGraphsTest(unittest.TestCase):
    def test_empty_graphs(self):
        """Does the ''merge_graphs'' function return an empty graph when given empty graphs?"""
        main_graph = UndirectedGraph()
        addition_graph = UndirectedGraph()

        node_map, edge_map = merge_graphs(main_graph, addition_graph)

        # --We expect no mapping whatsoever
        self.assertEqual({}, node_map)
        self.assertEqual({}, edge_map)

        # --We expect no nodes or edges in the main graph
        self.assertEqual(0, len(main_graph.nodes))
        self.assertEqual(0, len(main_graph.edges))

    def test_empty_addition_graph(self):
        """Does the ''merge_graphs'' function return a duplicate of the main
        graph when given an empty addition graph?"""
        original_graph = utility_functions.build_simple_test_graph()
        main_graph = copy.deepcopy(original_graph)
        addition_graph = UndirectedGraph()

        node_map, edge_map = merge_graphs(main_graph, addition_graph)

        # --We expect no mapping whatsoever
        self.assertEqual({}, node_map)
        self.assertEqual({}, edge_map)

        # --There should be the same number of nodes
        self.assertEqual(len(original_graph.get_all_node_ids()), len(main_graph.get_all_node_ids()))

        # --There should be the same number of edges
        self.assertEqual(len(original_graph.get_all_edge_ids()), len(main_graph.get_all_edge_ids()))

        # --All the nodes should match
        for node_id in original_graph.get_all_node_ids():
            original_node = original_graph.get_node(node_id)
            new_node = main_graph.get_node(node_id)

            # Verify each node has the proper number of edges
            self.assertEqual(len(original_node['edges']), len(new_node['edges']))

            # Verify each node has the right edges
            for edge_id in original_node['edges']:
                self.assertIn(edge_id, new_node['edges'])

        for edge_id in original_graph.get_all_edge_ids():
            original_edge = original_graph.get_edge(edge_id)
            new_edge = main_graph.get_edge(edge_id)

            # Verify each edge has the correct targets
            self.assertEqual(original_edge['vertices'], new_edge['vertices'])

    def test_empty_main_graph(self):
        """Does the ''merge_graphs'' function return a duplicate of the addition
        graph when given an empty main graph?"""
        original_graph = utility_functions.build_simple_test_graph()
        main_graph = UndirectedGraph()
        addition_graph = copy.deepcopy(original_graph)

        node_map, edge_map = merge_graphs(main_graph, addition_graph)

        # --We expect a 1-1 identity mapping
        expected_node_map = dict([(node_id, node_id) for node_id in original_graph.get_all_node_ids()])
        expected_edge_map = dict([(edge_id, edge_id) for edge_id in original_graph.get_all_edge_ids()])
        self.assertEqual(expected_node_map, node_map)
        self.assertEqual(expected_edge_map, edge_map)

        # --There should be the same number of nodes
        self.assertEqual(len(original_graph.get_all_node_ids()), len(main_graph.get_all_node_ids()))

        # --There should be the same number of edges
        self.assertEqual(len(original_graph.get_all_edge_ids()), len(main_graph.get_all_edge_ids()))

        # --All the nodes should match
        for node_id in original_graph.get_all_node_ids():
            original_node = original_graph.get_node(node_id)
            new_node = main_graph.get_node(node_id)

            # Verify each node has the proper number of edges
            self.assertEqual(len(original_node['edges']), len(new_node['edges']))

            # Verify each node has the right edges
            for edge_id in original_node['edges']:
                self.assertIn(edge_id, new_node['edges'])

        for edge_id in original_graph.get_all_edge_ids():
            original_edge = original_graph.get_edge(edge_id)
            new_edge = main_graph.get_edge(edge_id)

            # Verify each edge has the correct targets
            self.assertEqual(original_edge['vertices'], new_edge['vertices'])

    def test_simple_graph_copy(self):
        """Does the ''merge_graphs'' function produce a combined graph that maintains
        the correct topology for both components?"""
        original_graph = utility_functions.build_2_node_graph()
        addition_graph = build_triangle_graph()

        self.graph_copy_integrity_checker(original_graph, addition_graph)

    def test_complex_graph_copy(self):
        """Does the ''merge_graphs'' function produce a combined graph that maintains
        the correct topology for both components?"""
        original_graph = utility_functions.build_fully_biconnected_test_graph()
        addition_graph = build_triangle_graph()

        self.graph_copy_integrity_checker(original_graph, addition_graph)

    def graph_copy_integrity_checker(self, original_graph, addition_graph):
        """Utility function to test the integrity of a graph copy."""
        main_graph = copy.deepcopy(original_graph)

        node_map, edge_map = merge_graphs(main_graph, addition_graph)

        # --Verify that the updated graph has all the nodes and edges from both graphs
        expected_node_count = len(original_graph.get_all_node_ids()) + len(addition_graph.get_all_node_ids())
        expected_edge_count = len(original_graph.get_all_edge_ids()) + len(addition_graph.get_all_edge_ids())
        self.assertEqual(expected_node_count, len(main_graph.get_all_node_ids()))
        self.assertEqual(expected_edge_count, len(main_graph.get_all_edge_ids()))

        # --Verify that the original graph nodes and edges are still in-place
        for node_id in original_graph.get_all_node_ids():
            original_node = original_graph.get_node(node_id)
            new_node = main_graph.get_node(node_id)

            # Verify each node has the proper number of edges
            self.assertEqual(len(original_node['edges']), len(new_node['edges']))

            # Verify each node has the right edges
            for edge_id in original_node['edges']:
                self.assertIn(edge_id, new_node['edges'])

        for edge_id in original_graph.get_all_edge_ids():
            original_edge = original_graph.get_edge(edge_id)
            new_edge = main_graph.get_edge(edge_id)

            # Verify each edge has the correct targets
            self.assertEqual(original_edge['vertices'], new_edge['vertices'])

        # --Verify that the new nodes and edges exist and have the correct topology
        for node_id in addition_graph.get_all_node_ids():
            original_node = addition_graph.get_node(node_id)
            new_node = main_graph.get_node(node_map[node_id])

            # Verify each node has the proper number of edges
            self.assertEqual(len(original_node['edges']), len(new_node['edges']))

            # Verify each node has the right edges
            for edge_id in original_node['edges']:
                self.assertIn(edge_map[edge_id], new_node['edges'])

        for edge_id in addition_graph.get_all_edge_ids():
            original_edge = addition_graph.get_edge(edge_id)
            new_edge = main_graph.get_edge(edge_map[edge_id])

            # Verify each edge has the correct targets
            original_vertex_a, original_vertex_b = original_edge['vertices']
            mapped_new_vertices = (node_map[original_vertex_a], node_map[original_vertex_b])
            self.assertEqual(mapped_new_vertices, new_edge['vertices'])
