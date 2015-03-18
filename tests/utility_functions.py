"""Provides utility functions for unit testing."""

from ..graph import UndirectedGraph

def build_simple_test_graph():
	"""Builds a simple undirected graph that gets used for testing."""
	graph = UndirectedGraph()

	#There are 7 vertices in the test graph
	for _ in xrange(7):
		graph.new_node()

	#There are 4 edges in the test graph
	#--Edge: a
	graph.new_edge(1,2)
	#--Edge: b
	graph.new_edge(1,4)
	#--Edge: c
	graph.new_edge(2,5)
	#--Edge: d
	graph.new_edge(6,7)

	return graph

def build_single_node_graph():
	"""Builds a graph with a single node for testing."""
	graph = UndirectedGraph()
	graph.new_node()

	return graph

def build_2_node_graph():
	"""Builds a 2-node connected graph for testing."""
	graph = UndirectedGraph()

	graph.new_node()
	graph.new_node()
	graph.new_edge(1,2)

	return graph

def build_biconnected_test_graph():
	"""Builds a graph with multiple biconnected components that gets used for testing."""
	graph = UndirectedGraph()

	#There are 12 vertices in the test graph
	for _ in xrange(12):
		graph.new_node()

	#Nodes 1,2,3 form the first component
	graph.new_edge(1,2)
	graph.new_edge(1,3)
	graph.new_edge(2,3)

	#Nodes 4,5,6,7 form the second component
	graph.new_edge(4,5)
	graph.new_edge(4,6)
	graph.new_edge(5,6)
	graph.new_edge(5,7)
	graph.new_edge(6,7)

	#Nodes 8,9,10,11,12 form the third component
	graph.new_edge(8,9)
	graph.new_edge(8,10)
	graph.new_edge(8,11)
	graph.new_edge(8,12)
	graph.new_edge(9,10)
	graph.new_edge(10,11)
	graph.new_edge(10,12)
	graph.new_edge(11,12)

	#Nodes 2 and 5 connect the first and second components
	graph.new_edge(2,5)

	#Nodes 7 and 8 connect the second and third components
	graph.new_edge(7,8)

	return graph

def build_fully_biconnected_test_graph():
	"""Builds a graph with only one biconnected component that gets used for testing."""
	graph = build_biconnected_test_graph()

	#Connect the first and third components to create a ring, converting everything into a single biconnected component
	graph.new_edge(1,12)

	return graph
