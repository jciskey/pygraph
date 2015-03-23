"""Implements a Union/Find Disjoint Set class, used in other algorithms."""


class DisjointSet(object):
    """Implements an efficient disjoint set collection."""

    __label_counter = 0
    __set_counter = 0
    __forest = None

    def __init__(self):
        # We are using the implicit parent-pointer structure to store the trees
        self.__forest = {}

    def __len__(self):
        return self.__set_counter

    def __str__(self):
        return str(self.__forest)

    def add_set(self):
        """Adds a new set to the forest.
        Returns a label by which the new set can be referenced
        """
        self.__label_counter += 1
        new_label = self.__label_counter
        self.__forest[new_label] = -1  # All new sets have their parent set to themselves
        self.__set_counter += 1
        return new_label

    def find(self, node_label):
        """Finds the set containing the node_label.
        Returns the set label.
        """
        queue = []
        current_node = node_label
        while self.__forest[current_node] >= 0:
            queue.append(current_node)
            current_node = self.__forest[current_node]
        root_node = current_node

        # Path compression
        for n in queue:
            self.__forest[n] = root_node

        return root_node

    def union(self, label_a, label_b):
        """Joins two sets into a single new set.
        label_a, label_b can be any nodes within the sets
        """
        # Base case to avoid work
        if label_a == label_b:
            return

        # Find the tree root of each node
        root_a = self.find(label_a)
        root_b = self.find(label_b)

        # Avoid merging a tree to itself
        if root_a == root_b:
            return

        self.__internal_union(root_a, root_b)
        self.__set_counter -= 1

    def __internal_union(self, root_a, root_b):
        """Internal function to join two set trees specified by root_a and root_b.
        Assumes root_a and root_b are distinct.
        """
        # Merge the trees, smaller to larger
        update_rank = False
        # --Determine the larger tree
        rank_a = self.__forest[root_a]
        rank_b = self.__forest[root_b]
        if rank_a < rank_b:
            larger = root_b
            smaller = root_a
        else:
            larger = root_a
            smaller = root_b
            if rank_a == rank_b:
                update_rank = True
        # --Make the smaller tree a subtree of the larger tree
        self.__forest[smaller] = larger
        # --Update the rank of the new tree (if necessary)
        if update_rank:
            self.__forest[larger] -= 1
