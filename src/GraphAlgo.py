import json
import random
import sys
from asyncio.queues import PriorityQueue
from queue import PriorityQueue
import matplotlib.pyplot as plt
from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface


class GraphAlgo(GraphAlgoInterface):
    """"
    This class implements the interface of GraphAlgoInterface.
    The class includes a number of algorithms that run on directional weighted graphs.
    """

    def __init__(self, graph=DiGraph()):
        """Initializes a graph of DiGraph type"""
        self.graph = graph

    def get_graph(self):
        """
        @:return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str):
        """
        Loads a graph from a json file.
        @:param file_name /The path to the json file
        @:returns True if the loading was successful, False o.w.
        """
        ans = True
        try:
            with open(file_name, "r") as file:
                graph = DiGraph()
                dict = json.load(file)
                # The array of the nodes
                nodes = dict.get("Nodes")
                # The array of the edges
                edges = dict.get("Edges")
                for dictNodes in nodes:
                    # Adding a node with position
                    if dictNodes.get("pos") is not None:
                        pos = tuple(map(float, dictNodes.get("pos").split(',')))
                        graph.add_node(dictNodes.get("id"), pos)
                    # Adding a node with out position
                    else:
                        graph.add_node(dictNodes.get("id"))
                # Adding the edges to the graph
                for dictEdges in edges:
                    graph.add_edge(dictEdges.get("src"), dictEdges.get("dest"), dictEdges.get("w"))
                self.graph = graph
        except Exception as e:
            print(e)
            ans = False
        return ans

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @:param file_name/ The path to the out file
        @:return True if the save was successful, False o.w.
        """
        ans = True
        try:
            with open(file_name, "w") as file:
                # Convert the graph to a representation by a dictionary using as_dict_graph function
                json.dump(self.graph, default=lambda m: DiGraph.as_dict_graph(m), fp=file)
        except Exception as e:
            print(e)
            ans = False
        return ans

    def Dijkstra(self, key: int):
        """
        This function scanning this graph using the weight and the info of each node in the graph,
        start from the src node identified with some key.
        Returns a dictionary of nodes that are in the shortest path from a received node.
        @:param key : The key of src node
        @:return dictionary of keys of nodes
        """
        dict_parents = {}
        PQ = PriorityQueue()
        nodes = self.graph.get_all_v()
        # Update the weight of each node to infinity and update the color(info) of all the nodes to white.
        # White node - means we have not visited it yet.
        for node in nodes.values():
            node.setWeight(sys.maxsize)
            node.setInfo("White")
        # Update the node weight from which we will start scanning the graph to 0
        srcNode = nodes.get(key)
        srcNode.setWeight(0)
        PQ.put((srcNode.getWeight(), srcNode))
        # A loop that goes through all the nodes that we can reach to them
        # from the src node.
        while PQ.qsize() != 0:
            u = PQ.get()[1]
            # Black node - means we have updated the minimum weight of the node
            if u.getInfo() != "Black":
                for neighborKey in self.graph.all_out_edges_of_node(u.getKey()).keys():
                    neighborNode = nodes.get(neighborKey)
                    if neighborNode.getInfo() != "Black":
                        weight = self.graph.outEdges.get(u.getKey()).get(neighborKey) + u.getWeight()
                        # Update the min weight of each neighbor of node u.
                        if weight < neighborNode.getWeight():
                            neighborNode.setWeight(min(weight, neighborNode.getWeight()))
                            # Update the parent node of node neighbor to u.
                            dict_parents[neighborKey] = u.getKey()
                    # Add to the PQ the node with his current min weight
                    PQ.put((neighborNode.getWeight(), neighborNode))
            u.setInfo("Black")
        return dict_parents

    def BFS(self, key: int, regular: bool):
        """
       Returns an array of nodes that we can reach from the node of this node key
       @:param key : Key of node we search
       @:param status : True or False
       @:return array of nodes
       """
        helpList = []
        resultList = []
        nodes = self.graph.get_all_v()
        # Update the info of each node, besides the src node to white,
        # White node - means we have not visited it yet.
        for node in nodes.values():
            if node.getKey() == key:
                node.setInfo("Black")
                helpList.append(node)
                resultList.append(node)
            else:
                node.setInfo("White")
        # A loop that goes through all the nodes that we can reach to them
        # from the src node.
        while 0 < len(helpList):
            srcNode = helpList.pop(0)
            # regular graph
            if regular:
                dictKeys = self.graph.all_out_edges_of_node(srcNode.getKey()).keys()
            # "turn" the edges of the graph
            else:
                dictKeys = self.graph.all_in_edges_of_node(srcNode.getKey()).keys()
            for keyNi in dictKeys:
                neighborNode = nodes.get(keyNi)
                # If it is a node that we have not yet reached
                # and does not belong to any connected component
                if neighborNode.getInfo() == "White" and neighborNode.getTag != -1:
                    # Black node - means we were able to reach it from the src node
                    neighborNode.setInfo("Black")
                    helpList.append(neighborNode)
                    resultList.append(neighborNode)

        return resultList

    def connected_component(self, id1: int):
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @:param id1 The node of key=id
        @:return The list of nodes in the SCC
       """
        # nodes we were able to reach from the src node in the regular graph
        outList = self.BFS(id1, True)
        # nodes we were able to reach from the src node in the "transpose" graph
        self.BFS(id1, False)
        resultList = []
        # The connected component of the src node is the intersection between the above two groups
        for node in outList:
            # we not reached to this node in the transpose graph
            if node.getInfo() == "Black":
                resultList.append(node.getKey())
                # This node belongs to this connected_component
                node.setTag(-1)
        return sorted(resultList)

    def connected_components(self):
        """
       Finds all the Strongly Connected Component(SCC) in the graph.
       @:return The list all of SCC in this graph
      """
        # empty graph
        if self.graph.v_size() == 0:
            return []
        nodes = self.graph.get_all_v()
        # Update the all tag of node to maxsize-
        # means that no node yet belongs to any connected_component
        for node in nodes.values():
            node.setTag(sys.maxsize)
        listResult = []
        for node in nodes.values():
            # If the node already belongs to a connected_component
            if node.getTag() != -1:
                listResult.append(self.connected_component(node.getKey()))
        for node in nodes.values():
            node.setTag(sys.maxsize)
        return listResult

    def shortest_path(self, id1: int, id2: int):
        """
       Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
       @:param id1: The start node id
       @:param id2: The end node id
       @:return: The distance of the path, a list of the nodes ids that the path goes through
       """
        nodes = self.get_graph().get_all_v()
        # if one of the nodes do not exist in the graph
        if nodes.get(id1) is None or nodes.get(id2) is None:
            return float('inf'), []
        # The weight of the path from a node to itself is 0.
        if id1 == id2:
            return 0, [id1]
        # Run dijkstra on the src node
        dict_parents = self.Dijkstra(id1)
        if nodes.get(id2).getWeight() is sys.maxsize:
            return float('inf'), []
        list_path = []
        pathWeight = nodes.get(id2).getWeight()  # The weight of the path
        list_path.append(id2)
        key = dict_parents.get(id2)
        while key is not None:
            # Adding the nodes that are in this path
            list_path.insert(0, key)
            key = dict_parents.get(key)

        return pathWeight, list_path

    def plot_graph(self):
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @:return None
        """
        x = []
        y = []
        n = []
        x1 = 0
        y1 = 0
        nodes = self.graph.get_all_v()
        for node in nodes.keys():
            # If there is a node without pos
            if nodes.get(node).getPos() is None:
                edgeOut = self.graph.all_out_edges_of_node(node)
                if len(edgeOut) != 0:
                    # If his neighbors have pos ,take this sum pos
                    for key in edgeOut.keys():
                        if nodes.get(key).getPos() is not None:
                            x1 += nodes.get(key).getPos()[0]
                            y1 += nodes.get(key).getPos()[1]
                        else:
                            x1 = random.randint(0, 1000)
                            y1 = random.randint(0, 2000)
                    # Divided by the number of neighbors
                    pos = (x1 / len(edgeOut), y1 / len(edgeOut))
                    nodes.get(node).setPos(pos)  # Update the pos of the node

                elif len(edgeOut) == 0:
                    edgeIn = self.graph.all_in_edges_of_node(node)
                    # don't have neighbors we take a random pos
                    if len(edgeIn) == 0:
                        x1 = random.randint(0, 1000)
                        y1 = random.randint(0, 1000)
                    elif len(edgeIn) != 0:
                        for key in edgeIn.keys():
                            # If his neighbors have pos ,take this sum pos
                            if nodes.get(key).getPos() is not None:
                                x1 += nodes.get(key).getPos()[0]
                                y1 += nodes.get(key).getPos()[1]
                            else:
                                x1 = random.randint(0, 1000)
                                y1 = random.randint(0, 1000)
                        pos = (x1 / len(edgeIn), y1 / len(edgeIn))  # Divided by the number of edgeIn
                        self.graph.nodes.get(node).setPos(pos)  # Update the pos of the node
            # Adding the updated Corinthians of pos (x,y)
            x.append(nodes.get(node).getPos()[0])
            y.append(nodes.get(node).getPos()[1])

        fig, ax = plt.subplots()
        ax.scatter(x, y)

        for key in nodes.keys():
            n.append(key)

        # The key of node to put above each node in the graph
        for i, txt in enumerate(n):
            ax.annotate(n[i], (nodes.get(n[i]).getPos()[0], nodes.get(n[i]).getPos()[1]), color='red')

        # An arrow between the side of a node and its neighbor
        for node in nodes.keys():
            arrow_Out = self.graph.all_out_edges_of_node(node)
            for edge in arrow_Out.keys():
                if len(arrow_Out) != 0:
                    x_out = self.graph.nodes.get(edge).getPos()[0]
                    y_out = self.graph.nodes.get(edge).getPos()[1]
                    plt.annotate(s='', xy=(nodes.get(node).getPos()[0], nodes.get(node).getPos()[1]),
                                 xytext=(x_out, y_out),
                                 arrowprops=dict(arrowstyle="<|-"))

        plt.plot(x, y, "bo")
        plt.xlabel('x - axis')
        plt.ylabel('y - axis')
        plt.title("Graph Plot")
        plt.show()
        plt.close()
