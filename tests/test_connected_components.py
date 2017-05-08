"""Provides unit tests to verify that the connected components algorithm is functioning correctly."""

import unittest

from ..pygraph import UndirectedGraph, get_connected_components, get_connected_components_as_subgraphs, make_subgraph
from . import utility_functions


class ConnectedComponentsTest(unittest.TestCase):
    def test_correct_connected_components(self):
        """Does the ''connected_components'' function return the proper component breakdown for an undirected graph?"""
        # Build the test graph
        graph = utility_functions.build_simple_test_graph()

        # Known connected components
        component_a = [1, 2, 4, 5]
        component_b = [3]
        component_c = [6, 7]
        known_components = [component_a, component_b, component_c]

        # Pull the calculated connected components
        components = get_connected_components(graph)

        # Verify that the known connected components are in the calculated connected components
        # --There are 3 connected components in the test graph
        self.assertEqual(3, len(components))

        # --Verify each known component exists and has the correct number of nodes
        found_components_count = 0
        for kc in known_components:
            found_known_component = False
            for c in components:
                # --Determine if the current component is a superset of known component (it might
                # --have more nodes than the known component)
                superset_match = True
                for n in kc:
                    if n not in c:
                        # --This is not the correct component, go to the next one
                        superset_match = False
                        break
                if superset_match:
                    # --Determine if the current component has precisely the same number of nodes
                    # --in it as the known component
                    found_known_component = (len(kc) == len(c))
                if found_known_component:
                    found_components_count += 1
                    break
            if not found_known_component:
                # --We know the current component was not found in the connected components list,
                # --fail with an error message
                msg = 'Component {} not found in {}'.format(kc, components)
                self.fail(msg)

        # --This verifies that we found all three known components in the calculated components
        # --Prior tests should stop things before we get this far if there are errors,
        # --but it's a simple sanity check test
        self.assertEqual(3, found_components_count)

    def test_empty_connected_components(self):
        """Does the ''connected_components'' function return an empty list for an empty undirected graph?"""
        graph = UndirectedGraph()

        expected = []
        calculated = get_connected_components(graph)

        self.assertEqual(expected, calculated)

    def test_empty_cc_as_subgraphs(self):
        """Does the ''get_connected_components_as_subgraphs'' function return an empty list
         when given an empty graph?"""
        graph = UndirectedGraph()

        expected = []
        calculated = get_connected_components_as_subgraphs(graph)

        self.assertEqual(expected, calculated)

    def test_cc_as_subgraphs(self):
        """Does the ''get_connected_components_as_subgraphs'' function return a list of the proper subgraphs?"""
        graph = utility_functions.build_simple_test_graph()

        component_a_nodes = [1, 2, 4, 5]
        component_a_edges = [1, 2, 3]
        component_b_nodes = [3]
        component_b_edges = []
        component_c_nodes = [6, 7]
        component_c_edges = [4]

        component_a = make_subgraph(graph, component_a_nodes, component_a_edges)
        component_b = make_subgraph(graph, component_b_nodes, component_b_edges)
        component_c = make_subgraph(graph, component_c_nodes, component_c_edges)
        known_components = [component_a, component_b, component_c]

        # Pull the calculated connected components
        components = get_connected_components_as_subgraphs(graph)

        # Verify that the known connected components are in the calculated connected components
        # --There are 3 connected components in the test graph
        self.assertEqual(3, len(components))

        # --Verify each known component exists and has the correct number of nodes
        found_components_count = 0
        for kc in known_components:
            found_known_component = False
            for c in components:
                # --Determine if the current component is a superset of known component (it might
                # --have more nodes than the known component)
                node_superset_match = True
                edge_superset_match = True
                for n in kc.get_all_node_ids():
                    if n not in c.get_all_node_ids():
                        # --This is not the correct component, go to the next one
                        node_superset_match = False
                        break
                for e in kc.get_all_edge_ids():
                    if e not in c.get_all_edge_ids():
                        # --This is not the correct component, go to the next one
                        edge_superset_match = False
                if node_superset_match and edge_superset_match:
                    # --Determine if the current component has precisely the same number
                    # --of nodes and edges as the known component
                    found_known_component = ((len(kc.get_all_node_ids()) == len(c.get_all_node_ids())) and (
                        len(kc.get_all_edge_ids()) == len(c.get_all_edge_ids())))
                if found_known_component:
                    found_components_count += 1
                    break
            if not found_known_component:
                # --We know the current component was not found in the connected
                # --components list, fail with an error message
                component_string = '[{}]'.format(','.join(
                    ['(Nodes: {}, Edges: {})'.format(c.get_all_node_ids(), c.get_all_edge_ids()) for c in components]))
                msg = 'Component (Nodes: {}, Edges: {}) not found in {}'.format(kc.get_all_node_ids(),
                                                                                kc.get_all_edge_ids(), component_string)
                self.fail(msg)

        # --This verifies that we found all three known components in the calculated components
        # --Prior tests should stop things before we get this far if there are
        # --errors, but it's a simple sanity check test
        self.assertEqual(3, found_components_count)

