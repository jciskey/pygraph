"""Provides unit tests to verify that the biconnected components algorithms are functioning correctly."""

import unittest

from ..pygraph import (UndirectedGraph, find_biconnected_components, find_articulation_vertices, merge_graphs,
                     build_triangle_graph, build_square_graph, build_diamond_graph,
                     build_tetrahedral_graph, build_5_cycle_graph, build_gem_graph)

from . import utility_functions


class BiconnectedComponentsTest(unittest.TestCase):
    def test_empty_graph(self):
        """Does the ''find_biconnected_components'' function return an empty set of edges for an empty graph?"""
        graph = UndirectedGraph()

        expected = []
        calculated = find_biconnected_components(graph)

        self.assertEqual(expected, calculated)

    def test_single_node_graph(self):
        """Does the ''find_biconnected_components'' function return an empty set of edges for a graph with 1 node?"""
        graph = utility_functions.build_single_node_graph()

        expected = []
        calculated = find_biconnected_components(graph)

        self.assertEqual(expected, calculated)

    def test_2_node_graph(self):
        """Does the ''find_biconnected_components'' function return a single edge list for a 2-node connected graph?"""
        graph = utility_functions.build_2_node_graph()

        expected = [[1]]
        calculated = find_biconnected_components(graph)

        self.assertEqual(expected, calculated)

    def test_triangle_graph(self):
        """Does the ''find_biconnected_components'' function return a single edge list for a triangle graph?"""
        graph = build_triangle_graph()

        expected = [[1, 2, 3]]
        calculated = find_biconnected_components(graph)
        calculated[0].sort()

        self.assertEqual(expected, calculated)

    def test_square_graph(self):
        """Does the ''find_biconnected_components'' function return a single edge list for a square graph?"""
        graph = build_square_graph()

        expected = [[1, 2, 3, 4]]
        calculated = find_biconnected_components(graph)
        calculated[0].sort()

        self.assertEqual(expected, calculated)

    def test_diamond_graph(self):
        """Does the ''find_biconnected_components'' function return a single edge list for a diamond graph?"""
        graph = build_diamond_graph()

        expected = [[1, 2, 3, 4, 5]]
        calculated = find_biconnected_components(graph)
        calculated[0].sort()

        self.assertEqual(expected, calculated)

    def test_tetrahedral_graph(self):
        """Does the ''find_biconnected_components'' function return a single edge list for a tetrahedral graph?"""
        graph = build_tetrahedral_graph()

        expected = [[1, 2, 3, 4, 5, 6]]
        calculated = find_biconnected_components(graph)
        calculated[0].sort()

        self.assertEqual(expected, calculated)

    def test_5_cycle_graph(self):
        """Does the ''find_biconnected_components'' function return a single edge list for a 5-cycle graph?"""
        graph = build_5_cycle_graph()

        expected = [[1, 2, 3, 4, 5]]
        calculated = find_biconnected_components(graph)
        calculated[0].sort()

        self.assertEqual(expected, calculated)

    def test_gem_graph(self):
        """Does the ''find_biconnected_components'' function return a single edge list for a gem graph?"""
        graph = build_gem_graph()

        expected = [[1, 2, 3, 4, 5, 6, 7]]
        calculated = find_biconnected_components(graph)
        calculated[0].sort()

        self.assertEqual(expected, calculated)

    def test_fully_biconnected_graph(self):
        """Does the ''find_biconnected_components'' function correctly return
        the entire graph for a fully biconnected graph?"""
        graph = utility_functions.build_fully_biconnected_test_graph()

        expected_edges = range(1, 20)  # There are 19 edges in the test graph, so their IDs go from 1-19
        calculated_edges = find_biconnected_components(graph)

        # Verify that there is only a single component in the calculated edge list
        self.assertEqual(1, len(calculated_edges))

        # Verify all edges exist within the calculated edge list
        component = calculated_edges[0]
        for edge_id in expected_edges:
            self.assertIn(edge_id, component)

        # Verify that there are precisely the number of edges expected in the calculated edge list
        self.assertEqual(19, len(component))

    def test_biconnected_graph(self):
        """Does the ''find_biconnected_components'' function correctly identify the
        components in a graph with multiple biconnected components?"""
        graph = utility_functions.build_biconnected_test_graph()

        component_a = [1, 2, 3]
        component_b = [4, 5, 6, 7, 8]
        component_c = [9, 10, 11, 12, 13, 14, 15, 16]
        known_components = [component_a, component_b, component_c]

        calculated_components = find_biconnected_components(graph)

        # Verify that there are the expected number of components
        self.assertEqual(3, len(calculated_components))

        # --Verify each known component exists and has the correct number of edges
        found_components_count = 0
        for kc in known_components:
            found_known_component = False
            for c in calculated_components:
                # --Determine if the current component is a superset of known component
                # --(it might have more edges than the known component)
                superset_match = True
                for e in kc:
                    if e not in c:
                        # --This is not the correct component, go to the next one
                        superset_match = False
                        break
                if superset_match:
                    # --Determine if the current component has precisely the same number of
                    # --edges in it as the known component
                    found_known_component = (len(kc) == len(c))
                if found_known_component:
                    found_components_count += 1
                    break
            if not found_known_component:
                # --We know the current component was not found in the connected components
                # --list, fail with an error message
                msg = 'Component {} not found in {}'.format(kc, calculated_components)
                self.fail(msg)

        # --This verifies that we found all three known components in the calculated components
        # --Prior tests should stop things before we get this far if there are errors,
        # --but it's a simple sanity check test
        self.assertEqual(3, found_components_count)

    def test_disconnected_graph(self):
        """Does the ''find_biconnected_components'' function return components for each connected component?"""
        graph = utility_functions.build_biconnected_test_graph()
        addition_graph = build_triangle_graph()

        node_map, edge_map = merge_graphs(graph, addition_graph)

        calculated_components = find_biconnected_components(graph)

        # Verify that there are the expected number of components
        self.assertEqual(4, len(calculated_components))


class ArticulationVerticesTest(unittest.TestCase):
    def test_articulation_vertices_empty_graph(self):
        """Does the ''find_articulation_vertices'' function return an empty list when run on an empty graph?"""
        graph = UndirectedGraph()

        expected = []
        calculated = find_articulation_vertices(graph)

        self.assertEqual(expected, calculated)

    def test_articulation_vertices_fully_biconnected_graph(self):
        """Does the ''find_articulation_vertices'' function return an empty list
        when run on a fully biconnected graph?"""
        graph = utility_functions.build_fully_biconnected_test_graph()

        expected = []
        calculated = find_articulation_vertices(graph)

        self.assertEqual(expected, calculated)

    def test_articulation_vertices_single_cut_vertex(self):
        """Does the ''find_articulation_vertices'' function return a single
        articulation vertex for a graph with a single cut vertex?"""
        graph = utility_functions.build_3_node_line_graph()

        expected = [2]
        calculated = find_articulation_vertices(graph)

        self.assertEqual(expected, calculated)

    def test_articulation_vertices_single_cut_vertex_is_root(self):
        """Does the ''find_articulation_vertices'' function return a single
        articulation vertex for a graph where the root node is the single cut vertex?"""
        graph = utility_functions.build_3_node_line_root_articulation_graph()

        expected = [1]
        calculated = find_articulation_vertices(graph)

        self.assertEqual(expected, calculated)

    def test_articulation_vertices_dual_cut_vertices(self):
        """Does the ''find_articulation_vertices'' function return a pair of
        articulation vertices for a graph where there are two?"""
        graph = utility_functions.build_simple_test_graph()

        expected = [1, 2]
        calculated = find_articulation_vertices(graph)
        calculated.sort()

        self.assertEqual(expected, calculated)

    def test_articulation_vertices_biconnected_graph(self):
        """Does the ''find_articulation_vertices'' function return the correct list
        of articulation vertices for a graph with multiple biconnected components?"""
        graph = utility_functions.build_biconnected_test_graph()

        expected = [2, 5, 7, 8]
        calculated = find_articulation_vertices(graph)
        calculated.sort()

        self.assertEqual(expected, calculated)

