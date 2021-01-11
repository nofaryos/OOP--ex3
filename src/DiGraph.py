from GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    """ This class implements the interfaces of GraphInterface,
   It is designed to create an directional weighted graph.
   Each graph has dictionary of nodes, inEdges and outEdges, num of edges and num
   of changes that made on the graph(MC).
   The creation of the graph requires the use of vertex-type objects,
   this object is realized as an internal private class in this class."""

    def __init__(self):
        """Initialize the properties of the graph"""
        self.nodes = {}
        self.inEdges = {}
        self.outEdges = {}
        self.MC = 0
        self.edgesNum = 0

    def v_size(self):
        """
        Returns the number of nodes in this graph
        @:return The number of nodes in this graph
        """
        return len(self.nodes)

    def e_size(self):
        """
         Returns the number of edges in this graph
         @:return The number of edges in this graph
         """
        return self.edgesNum

    def get_all_v(self):
        """
        return a dictionary of all the nodes in the Graph, each node is represented using a pair
        (node_id, node_data)
        @:return dictionary of pairs of keys and nodes.
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int):
        """
        Return a dictionary of all the nodes connected to (into) node_id,
        each node is represented using a pair (other_node_id, weight)
        @:param id1: the key of the node
        @:return: dictionary of nodes
        """
        return self.inEdges.get(id1)

    def all_out_edges_of_node(self, id1: int):
        """
        Return a dictionary of all the nodes connected from node_id, each node is represented using a pair
        (other_node_id, weight)
        @:param id1: the key of the node
        @:return: dictionary of nodes
        """
        return self.outEdges.get(id1)

    def get_mc(self):
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @:return The number of changes made to the graph
        """
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float):
        """
       Adds an edge to the graph.
       @param id1: The key of the start node of the edge
       @param id2: The key of the end node of the edge
       @param weight: The weight of the edge
       @:return True if the edge was added successfully, False o.w.
       """
        # # If it's the same node or if the weight lower than zero,
        # we will not add edge
        if id1 != id2 and 0 <= weight:
            # The two nodes in the graph
            if self.nodes.get(id1) is not None and self.nodes.get(id2) is not None:
                edge = self.outEdges.get(id1).get(id2)
                # There is an edge between the two nodes
                if edge is not None:
                    return
                self.outEdges.get(id1)[id2] = weight
                self.inEdges.get(id2)[id1] = weight
                self.MC += 1  # We will count a change
                self.edgesNum += 1  # We will add edge
                return True
            return False
        return False

    def add_node(self, node_id: int, pos: tuple = None):
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @:return True if the node was added successfully, False o.w.
        """
        # This node is already exits in the graph
        if self.nodes.get(node_id) is not None:
            return False
        # Adding the node
        self.nodes[node_id] = DiGraph.nodeData(node_id, pos)
        # Create new dictionaries for the edges of the new node
        self.inEdges[node_id] = {}
        self.outEdges[node_id] = {}
        self.MC += 1
        return True

    def remove_node(self, node_id: int):
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @:return True if the node was removed successfully, False o.w.
        """
        if self.nodes.get(node_id) is None:
            return False
        # All the keys that has a edgeOut between them and node_id
        keysOut = list(self.outEdges.get(node_id).keys())
        for i in range(len(keysOut)):
            # Removing the edge between node_id to keysOut(i)
            DiGraph.remove_edge(self, node_id, keysOut[i])
        # All the keys that has a edgeIn between them and node_id
        keysIn = list(self.inEdges.get(node_id).keys())
        for i in range(len(keysIn)):
            # Removing the edge between keysIn(i) to node_id
            DiGraph.remove_edge(self, keysIn[i], node_id)
        # Removing this node
        del self.inEdges[node_id]
        del self.outEdges[node_id]
        del self.nodes[node_id]
        self.MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int):
        """
        Removes an edge from the graph.
        @param node_id1: The key of the start node of the edge
        @param node_id2: The key of the end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        """
        if self.nodes.get(node_id1) is None or self.nodes.get(node_id2) is None:
            return False
        # There is a edge between node_id1 to node_id2
        if self.outEdges.get(node_id1).get(node_id2) is not None:
            #  Removing the edge from outEdges and inEdges
            del self.outEdges.get(node_id1)[node_id2]
            del self.inEdges.get(node_id2)[node_id1]
            self.edgesNum -= 1
            self.MC += 1
            return True

    def as_array_edges(self):
        """Returns an array of edges for each edge there is:
         src node, dest node and edge weight"""
        edges_array = []
        try:
            # We will go over the dictionary of out edge
            for key in self.outEdges.keys():
                # If this node has out edge
                if len(self.outEdges.get(key)) > 0:
                    dict = self.outEdges.get(key)
                    for k in dict.keys():
                        if dict.get(k) is not None:
                            src = key
                            dest = k
                            weight = dict.get(k)
                            edges_array.append({"src": src, "dest": dest, "w": weight})
        except Exception as e:
            print(e)
        return edges_array

    def as_array_nodes(self):
        """Returns an array of nodes"""
        nodes_array = []
        try:
            # Information about the node from the
            # function as_dict in nodeData class
            for v in self.nodes.values():
                nodes_array.append(DiGraph.nodeData.as_dict(v))
        except Exception as e:
            print(e)
        return nodes_array

    def as_dict_graph(self):
        """Returns a dictionary Representing jason of the graph with the nodes and edges of that graph
        @:return dictionary of a graph"""
        graph_dict = {}
        try:
            graph_dict["Nodes"] = DiGraph.as_array_nodes(self)  # Array on nodes
            graph_dict["Edges"] = DiGraph.as_array_edges(self)  # Array on edges
        except Exception as e:
            print(e)
        return graph_dict

    def __eq__(self, other):
        """Checks if two graphs are equal
        @:param other Graph
        @:return True If the graphs are equal, False o.w.
        """
        if isinstance(other, DiGraph):
            # check if the number of nodes in the graphs are equal
            if self.v_size() != other.v_size() or self.e_size() != other.e_size():
                return False
            # Checking if the nodes of the two graphs are equals
            ans = self.get_all_v() == other.get_all_v()
            if ans:
                # Checking if the edges of the two graphs are equals
                for key in self.nodes.keys():
                    ans = self.all_out_edges_of_node(key) == other.all_out_edges_of_node(key)
                    if not ans:
                        return ans
            return True
        return False

    def __str__(self):
        """Return string a graph with all its information
         @:return string of graph"""
        return f"num of nodes:{len(self.nodes)}\nnum of edges:{self.edgesNum}\nnodes:{self.nodes}\nedges:{self.outEdges}"

    class nodeData:
        """
       This class represents a vertex in  a directional weighted graph.
       Each node has an identity number(unique key), color(info), weight, position
       and tag that represents it in a particular graph.
       """

        def __init__(self, key: int, pos: tuple = None):
            """Initialize the properties of the node"""
            self.pos = pos
            self.key = key
            self.tag = 0
            self.info = " "
            self.weight = 0

        def getKey(self):
            """Returns the node key
        @:return the node key"""
            return self.key

        def getInfo(self):
            """Returns the node info
           @:return the node info"""
            return self.info

        def setInfo(self, info: str):
            """Updating the info of node
           @:param info: Info of node"""
            self.info = info

        def getTag(self):
            """Returns the tag of node
           @: return: the tag of the node"""
            return self.tag

        def setTag(self, tag: int):
            """Updating the tag of node
           @:param tag: Info of node"""
            self.tag = tag

        def getPos(self):
            """Returns the node pos
           @:return the node of pos"""
            return self.pos

        def setPos(self, pos: tuple):
            """Updating the pos of node
           @:param pos : The pos of node"""
            self.pos = pos

        def getWeight(self):
            """Returns the node weight
           @:return the node of weight"""
            return self.weight

        def setWeight(self, weight: float):
            """Updating the pos of node
           @:param weight : The weight of node"""
            self.weight = weight

        def __eq__(self, other):
            """Checks if two nodes are equal
           @:param other node
           @:return True If the nodes are equal, False o.w.
           """
            if isinstance(other, DiGraph.nodeData):
                # Two nodes is equals if they have the same key
                return self.key == other.key
            return False

        def __str__(self) -> str:
            """Return string a node with all its information
           @:return string of node"""
            return f"key:{self.key}, pos:{self.pos}, tag:{self.tag}, info:{self.info}"

        def __repr__(self) -> str:
            """Returns information of several nodes in a particular collection
           @:return information of several nodes in a particular collection """
            return f"key:{self.key}, pos:{self.pos}, tag:{self.tag}, info:{self.info}"

        def as_dict(self):
            """Returns a dictionary of node containing key and pos
           @:return dictionary of node"""
            node_dict = {}
            try:
                if self.pos is not None:
                    node_dict["pos"] = f"{self.pos[0]},{self.pos[1]},{self.pos[2]}"  # position of node
                node_dict["id"] = self.key  # key of node
            except Exception as e:
                print(e)
            return node_dict
