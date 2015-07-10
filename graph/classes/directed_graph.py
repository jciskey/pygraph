"""Implements the functionality of a directed graph."""

import copy

from ..exceptions import NonexistentNodeError, NonexistentEdgeError


class DirectedGraph(object):
    nodes = None
    edges = None
    next_node_id = 1
    next_edge_id = 1

    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self._num_nodes = 0
        self._num_edges = 0

    def __deepcopy__(self, memo=None):
        graph = DirectedGraph()
        graph.nodes = copy.deepcopy(self.nodes)
        graph.edges = copy.deepcopy(self.edges)
        graph.next_node_id = self.next_node_id
        graph.next_edge_id = self.next_edge_id
        graph._num_nodes = self._num_nodes
        graph._num_edges = self._num_edges
        return graph

    def num_nodes(self):
        """Returns the current number of nodes in the graph."""
        return self._num_nodes

    def num_edges(self):
        """Returns the current number of edges in the graph."""
        return self._num_edges

    def generate_node_id(self):
        node_id = self.next_node_id
        self.next_node_id += 1
        return node_id

    def generate_edge_id(self):
        edge_id = self.next_edge_id
        self.next_edge_id += 1
        return edge_id

    def new_node(self):
        """Adds a new, blank node to the graph.
        Returns the node id of the new node."""
        node_id = self.generate_node_id()

        node = {'id': node_id,
                'edges': [],
                'data': {}
        }

        self.nodes[node_id] = node

        self._num_nodes += 1

        return node_id

    def new_edge(self, node_a, node_b, cost=1):
        """Adds a new edge from node_a to node_b that has a cost.
        Returns the edge id of the new edge."""

        # Verify that both nodes exist in the graph
        try:
            self.nodes[node_a]
        except KeyError:
            raise NonexistentNodeError(node_a)
        try:
            self.nodes[node_b]
        except KeyError:
            raise NonexistentNodeError(node_b)

        # Create the new edge
        edge_id = self.generate_edge_id()

        edge = {'id': edge_id,
                'vertices': (node_a, node_b),
                'cost': cost,
                'data': {}
        }

        self.edges[edge_id] = edge
        self.nodes[node_a]['edges'].append(edge_id)

        self._num_edges += 1

        return edge_id

    def neighbors(self, node_id):
        """Find all the nodes where there is an edge from the specified node to that node.
        Returns a list of node ids."""
        node = self.get_node(node_id)
        return [self.get_edge(edge_id)['vertices'][1] for edge_id in node['edges']]

    def adjacent(self, node_a, node_b):
        """Determines whether there is an edge from node_a to node_b.
        Returns True if such an edge exists, otherwise returns False."""
        neighbors = self.neighbors(node_a)
        return node_b in neighbors

    def edge_cost(self, node_a, node_b):
        """Returns the cost of moving between the edge that connects node_a to node_b.
        Returns +inf if no such edge exists."""
        cost = float('inf')
        node_object_a = self.get_node(node_a)
        for edge_id in node_object_a['edges']:
            edge = self.get_edge(edge_id)
            tpl = (node_a, node_b)
            if edge['vertices'] == tpl:
                cost = edge['cost']
                break
        return cost

    def get_node(self, node_id):
        """Returns the node object identified by "node_id"."""
        try:
            node_object = self.nodes[node_id]
        except KeyError:
            raise NonexistentNodeError(node_id)
        return node_object

    def get_all_node_ids(self):
        """Returns a list of all the node ids in the graph."""
        return self.nodes.keys()

    def get_all_node_objects(self):
        """Returns a list of all the node objects in the graph."""
        return self.nodes.values()

    def get_edge(self, edge_id):
        """Returns the edge object identified by "edge_id"."""
        try:
            edge_object = self.edges[edge_id]
        except KeyError:
            raise NonexistentEdgeError(edge_id)
        return edge_object

    def get_all_edge_ids(self):
        """Returns a list of all the edge ids in the graph"""
        return self.edges.keys()

    def get_all_edge_objects(self):
        """Returns a list of all the edge objects in the graph."""
        return self.edges.values()

    def delete_edge_by_id(self, edge_id):
        """Removes the edge identified by "edge_id" from the graph."""
        edge = self.get_edge(edge_id)

        # Remove the edge from the "from node"
        # --Determine the from node
        from_node_id = edge['vertices'][0]
        from_node = self.get_node(from_node_id)

        # --Remove the edge from it
        from_node['edges'].remove(edge_id)

        # Remove the edge from the edge list
        del self.edges[edge_id]

        self._num_edges -= 1

    def delete_edge_by_nodes(self, node_a, node_b):
        """Removes all the edges from node_a to node_b from the graph."""
        node = self.get_node(node_a)

        # Determine the edge ids
        edge_ids = []
        for e_id in node['edges']:
            edge = self.get_edge(e_id)
            if edge['vertices'][1] == node_b:
                edge_ids.append(e_id)

        # Delete the edges
        for e in edge_ids:
            self.delete_edge_by_id(e)

    def delete_node(self, node_id):
        """Removes the node identified by node_id from the graph."""
        node = self.get_node(node_id)

        # Remove all edges from the node
        for e in node['edges']:
            self.delete_edge_by_id(e)

        # Remove all edges to the node
        edges = [edge_id for edge_id, edge in self.edges.items() if edge['vertices'][1] == node_id]
        for e in edges:
            self.delete_edge_by_id(e)

        # Remove the node from the node list
        del self.nodes[node_id]

        self._num_nodes -= 1

    def move_edge_source(self, edge_id, node_a, node_b):
        """Moves an edge originating from node_a so that it originates from node_b."""
        # Grab the edge
        edge = self.get_edge(edge_id)

        # Alter the vertices
        edge['vertices'] = (node_b, edge['vertices'][1])

        # Remove the edge from node_a
        node = self.get_node(node_a)
        node['edges'].remove(edge_id)

        # Add the edge to node_b
        node = self.get_node(node_b)
        node['edges'].append(edge_id)

    def move_edge_target(self, edge_id, node_a):
        """Moves an edge so that it targets node_a."""
        # Grab the edge
        edge = self.get_edge(edge_id)

        # Alter the vertices
        edge['vertices'] = (edge['vertices'][0], node_a)

    def get_edge_ids_by_node_ids(self, node_a, node_b):
        """Returns a list of edge ids connecting node_a to node_b."""
        # Check if the nodes are adjacent
        if not self.adjacent(node_a, node_b):
            return []

        # They're adjacent, so pull the list of edges from node_a and determine which ones point to node_b
        node = self.get_node(node_a)
        return [edge_id for edge_id in node['edges'] if self.get_edge(edge_id)['vertices'][1] == node_b]

    def get_first_edge_id_by_node_ids(self, node_a, node_b):
        """Returns the first (and possibly only) edge connecting node_a and node_b."""
        ret = self.get_edge_ids_by_node_ids(node_a, node_b)
        if not ret:
            return None
        else:
            return ret[0]
