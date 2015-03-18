"""Implements the functionality of an undirected graph."""

import copy

from .directed_graph import DirectedGraph

class UndirectedGraph(DirectedGraph):

	def __deepcopy__(self, memo=None):
		graph = UndirectedGraph()
		graph.nodes = copy.deepcopy(self.nodes)
		graph.edges = copy.deepcopy(self.edges)
		graph.next_node_id = self.next_node_id
		graph.next_edge_id = self.next_edge_id
		return graph

	def new_edge(self, node_a, node_b):
		"""Adds a new, undirected edge between node_a and node_b.
		Returns the edge id of the new edge."""
		edge_id = super(UndirectedGraph, self).new_edge(node_a, node_b)
		self.nodes[node_b]['edges'].append(edge_id)
		return edge_id

	def neighbors(self, node_id):
		"""Find all the nodes where there is an edge from the specified node to that node.
		Returns a list of node ids."""
		node = self.get_node(node_id)
		flattened_nodes_list = []
		for a, b in [self.get_edge(edge_id)['vertices'] for edge_id in node['edges']]:
			flattened_nodes_list.append(a)
			flattened_nodes_list.append(b)
		node_set = set(flattened_nodes_list)
		if node_id in node_set:
			node_set.remove(node_id)
		return [nid for nid in node_set]

	def delete_edge_by_id(self, edge_id):
		"""Removes the edge identified by "edge_id" from the graph."""
		edge = self.edges[edge_id]

		#Remove the edge from the "from node"
		#--Determine the from node
		from_node_id = edge['vertices'][0]
		from_node = self.get_node(from_node_id)

		#--Remove the edge from it
		from_node['edges'].remove(edge_id)

		#Remove the edge from the "to node"
		to_node_id = edge['vertices'][1]
		to_node = self.get_node(to_node_id)

		#--Remove the edge from it
		to_node['edges'].remove(edge_id)

		#Remove the edge from the edge list
		del self.edges[edge_id]

	def move_edge_target(self, edge_id, node_a):
		"""Moves an edge so that it targets node_a."""
		#Grab the edge
		edge = self.get_edge(edge_id)

		#Remove the edge from the original "target node"
		original_target_node_id = edge['vertices'][1]
		original_target_node = self.get_node(original_target_node_id)
		original_target_node['edges'].remove(edge_id)

		#Add the edge to the new target node
		new_target_node_id = node_a
		new_target_node = self.get_node(new_target_node_id)
		new_target_node['edges'].append(edge_id)

		#Alter the vertices on the edge
		edge['vertices'] = (edge['vertices'][0], node_a)
