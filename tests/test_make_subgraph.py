"""Provides unit tests to verify that the make subgraph algorithm is functioning correctly."""

import unittest

from ..pygraph import UndirectedGraph, make_subgraph
from . import utility_functions


class MakeSubgraphTest(unittest.TestCase):
    def test_empty_graph(self):
        """Does the ''make_subgraph'' function return an empty graph when given an empty graph?"""
        graph = UndirectedGraph()

        subgraph = make_subgraph(graph, [], [])

        self.assertEqual(0, len(subgraph.nodes))
        self.assertEqual(0, len(subgraph.edges))

    def test_simple_graph_copy(self):
        """Does the ''make_subgraph'' function return a duplicate graph when given
        all the nodes and edges from the graph?"""
        graph = utility_functions.build_simple_test_graph()

        subgraph = make_subgraph(graph, graph.get_all_node_ids(), graph.get_all_edge_ids())

        # There are 7 nodes
        self.assertEqual(7, len(subgraph.nodes))

        # There are 4 edges
        self.assertEqual(4, len(subgraph.edges))

        for node_id in graph.nodes:
            original_node = graph.get_node(node_id)
            new_node = subgraph.get_node(node_id)

            # Verify each node has the proper number of edges
            self.assertEqual(len(original_node['edges']), len(new_node['edges']))

            # Verify each node has the right edges
            for edge_id in original_node['edges']:
                self.assertIn(edge_id, new_node['edges'])

        for edge_id in graph.get_all_edge_ids():
            original_edge = graph.get_edge(edge_id)
            new_edge = subgraph.get_edge(edge_id)

            # Verify each edge has the correct targets
            self.assertEqual(original_edge['vertices'], new_edge['vertices'])

    def test_subgraph_copy(self):
        """Does the ''make_subgraph'' function create the correct subgraph when given a list of nodes and edges?"""
        graph = utility_functions.build_simple_test_graph()

        expected_nodes = [1, 2, 4, 6, 7]
        expected_edges = [1, 2, 4]

        subgraph = make_subgraph(graph, expected_nodes, expected_edges)

        # --Node 1 should have 2 edges (IDs: 1,2)
        # --Node 2 should have 1 edge (IDs: 1)
        # --Node 4 should have 1 edge (IDs: 2)
        # --Node 6 should have 1 edge (IDs: 4)
        # --Node 7 should have 1 edge (IDs: 4)
        node_check_pairs = [
            # These pairs have the form: (node_id, edge_ids)
            (1, (1, 2)),
            (2, (1,)),
            (4, (2,)),
            (6, (4,)),
            (7, (4,)),
        ]

        for node_id, edge_ids in node_check_pairs:
            node = subgraph.get_node(node_id)
            self.assertEqual(len(edge_ids), len(node['edges']))
            for eid in edge_ids:
                self.assertIn(eid, node['edges'])

        # --Edge 1 should connect nodes 1 and 2
        # --Edge 2 should connect nodes 1 and 4
        # --Edge 4 should connect nodes 6 and 7
        edge_check_pairs = [
            # These pairs have the form: (edge_id, (node_id, node_id))
            (1, (1, 2)),
            (2, (1, 4)),
            (4, (6, 7)),
        ]

        for edge_id, tpl in edge_check_pairs:
            edge = subgraph.get_edge(edge_id)
            self.assertEqual(tpl, edge['vertices'])