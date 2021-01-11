import json
import random
import time
from unittest import TestCase
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
import networkx as nx


# function for creating graph
def createGraph(n):
    graph = DiGraph()
    for i in range(n):
        graph.add_node(i)
    return graph


class TestGraphAlgo(TestCase):

    def test_load_from_json_1(self):
        graph = createGraph(50)
        graph1 = GraphAlgo(graph)
        graph.add_edge(10, 20, 0)
        graph.add_edge(1, 3, 5)
        graph.add_edge(4, 5, 6)
        graph.add_edge(7, 8, 9)

        # save the graph
        self.assertTrue(graph1.save_to_json("graph"))
        graph2 = GraphAlgo(graph)

        # load the graph
        self.assertTrue(graph2.load_from_json("graph"))

        # the graphs should be equals
        self.assertEqual(graph1.get_graph(), graph2.get_graph())

        # the graphs should be different after removing node from just one of them
        graph.remove_node(0)
        self.assertNotEqual(graph1.get_graph(), graph2.get_graph())

    def test_json_save_and_lode_2(self):
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)

        # save and load graph with nodes with position
        for i in range(50):
            graph.add_node(i, (4.6777, 7.7888, 9.95555))
        self.assertTrue(graph_algo.save_to_json("graph_test_1"))
        self.assertTrue(graph_algo.load_from_json("graph_test_1"))
        self.assertTrue(graph == graph_algo.get_graph())
        graph.remove_node(40)
        self.assertFalse(graph == graph_algo.get_graph())

        # save and load big graph
        graph = DiGraph()
        for i in range(100):
            graph.add_node(i, (i, i + 2, i + 3))
        for i in range(100):
            graph.add_edge(i, 5, i + 5)
            graph.add_edge(i, 10, i + 10)
            graph.add_edge(i, 15, i + 15)
            graph.add_edge(i, 20, i + 20)
        graph_algo = GraphAlgo(graph)
        self.assertTrue(graph_algo.save_to_json("graph_test_2"))
        self.assertTrue(graph_algo.load_from_json("graph_test_2"))
        self.assertTrue(graph == graph_algo.get_graph())

        # empty graph test
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        self.assertTrue(graph_algo.save_to_json("graph_test_3"))
        self.assertTrue(graph_algo.load_from_json("graph_test_3"))
        self.assertTrue(graph == graph_algo.get_graph())

    def test_connected_component(self):
        # connected_component in graph without edges
        graph = createGraph(15)
        graphAlgo = GraphAlgo(graph)
        nodes = graph.get_all_v()
        list_0 = [0]
        self.assertListEqual(list_0, graphAlgo.connected_component(0))

        # connected_component of node that do not exist in the graph
        list_empty = []
        self.assertListEqual(list_empty, graphAlgo.connected_component(50))

        # creating connected_component
        graph.add_edge(0, 4, 7)
        graph.add_edge(0, 7, 8)
        graph.add_edge(7, 0, 6)
        graph.add_edge(4, 0, 6)
        graph.add_edge(1, 2, 8)
        graph.add_edge(2, 1, 9)
        graphAlgo = GraphAlgo(graph)
        list_0 = graphAlgo.connected_component(0)
        self.assertEqual(3, len(list_0))
        self.assertFalse(list_0.__contains__(2))
        self.assertTrue(list_0.__contains__(4))
        self.assertTrue(list_0.__contains__(7))
        graph.add_edge(4, 1, 9)
        list_0 = graphAlgo.connected_component(0)
        self.assertFalse(list_0.__contains__(1))
        graph.add_edge(1, 4, 9)
        list_0 = graphAlgo.connected_component(0)
        self.assertTrue(list_0.__contains__(1))
        self.assertTrue(list_0.__contains__(2))
        graph.remove_node(0)
        self.assertListEqual(list_empty, graphAlgo.connected_component(0))

    def test_connected_components(self):
        graph = createGraph(6)
        graphAlgo = GraphAlgo(graph)

        # graph with out edges
        self.assertEqual(6, len(graphAlgo.connected_components()))

        # Check that the connected_components of the
        # graph include the connected_component of one of the nodes in the graph
        self.assertTrue(graphAlgo.connected_components().__contains__(graphAlgo.connected_component(3)))

        # one edge connection does not change the connected_components
        graph.add_edge(0, 5, 1)

        self.assertEqual(6, len(graphAlgo.connected_components()))

        # creating SCC of 5 and 0 nodes
        graph.add_edge(5, 0, 1)
        self.assertEqual(5, len(graphAlgo.connected_components()))
        self.assertTrue(graphAlgo.connected_components().__contains__(graphAlgo.connected_component(0)))

        # creating more SCC
        graph.add_edge(5, 2, 0)
        graph.add_edge(2, 5, 0)
        graph.add_edge(1, 2, 0)
        graph.add_edge(2, 1, 0)
        self.assertEqual(3, len(graphAlgo.connected_components()))
        graph.add_edge(1, 3, 7)
        graph.add_edge(3, 1, 7)
        self.assertEqual(2, len(graphAlgo.connected_components()))
        graph.add_edge(4, 5, 7)
        graph.add_edge(5, 4, 7)
        self.assertEqual(1, len(graphAlgo.connected_components()))
        graph.remove_node(0)
        self.assertEqual(1, len(graphAlgo.connected_components()))
        graph.remove_edge(1, 3)
        self.assertEqual(2, len(graphAlgo.connected_components()))
        graphAlgo.connected_component(0)

    def test_shortest_path(self):
        graph = createGraph(5)
        graphAlgo = GraphAlgo(graph)
        graph.add_edge(0, 1, 1.5)
        graph.add_edge(1, 2, 0.5)
        graph.add_edge(2, 3, 0.5)
        graph.add_edge(0, 3, 6.5)
        graph.add_edge(3, 4, 6.5)

        # short path between node to himself
        self.assertEqual((0, [0]), graphAlgo.shortest_path(0, 0))

        # short path between two nodes that do not exist in the graph
        self.assertEqual((float('inf'), []), graphAlgo.shortest_path(10, 20))

        # short path between node that exist in the graph to node that do not exist in the graph
        self.assertEqual((float('inf'), []), graphAlgo.shortest_path(0, 20))

        # short path between two nodes that exist in the graph

        self.assertEqual((2.5, [0, 1, 2, 3]), graphAlgo.shortest_path(0, 3))

        # remove an edge from the path
        graph.remove_edge(1, 2)
        self.assertEqual((6.5, [0, 3]), graphAlgo.shortest_path(0, 3))

        # connect new edges
        graph.add_edge(2, 0, 8)
        graph.add_edge(4, 0, 0.5)
        self.assertEqual((7.5, [2, 3, 4, 0]), graphAlgo.shortest_path(2, 0))

    # Functions for comparisons

    def test_load_graphs(self):
        listMyShortPath = []
        listNxShortPath = []
        listMyBFS = []
        listNxBFS = []
        listMyDijkstra = []
        listNxDijkstra = []
        listMyConnected_components = []
        listNxConnected_components = []
        listMyConnected_component = []
        graph = DiGraph()
        myGraph = GraphAlgo(graph)
        myGraph.load_from_json("../data/G_10_80_1.json")
        nxGraph = load_networkX(self, "../data/G_10_80_1.json")

        x, y = test_shortPath(self, myGraph, nxGraph, 100)
        listMyShortPath.insert(0, x)
        listNxShortPath.insert(0, y)

        x, y = test_BFS(self, myGraph, nxGraph, 100)
        listMyBFS.insert(0, x)
        listNxBFS.insert(0, y)
        x, y = test_Dijkstra(self, myGraph, nxGraph, 100)
        listMyDijkstra.insert(0, x)
        listNxDijkstra.insert(0, y)
        x, y = test_connected_components(self, myGraph, nxGraph)
        listMyConnected_components.insert(0, x)
        listNxConnected_components.insert(0, y)
        x = test_connected_component(self, myGraph, 100)
        listMyConnected_component.insert(0, x)

        myGraph.load_from_json("../data/G_100_800_1.json")
        nxGraph = load_networkX(self, "../data/G_100_800_1.json")

        x, y = test_shortPath(self, myGraph, nxGraph, 100)
        listMyShortPath.insert(1, x)
        listNxShortPath.insert(1, y)
        x, y = test_BFS(self, myGraph, nxGraph, 100)
        listMyBFS.insert(1, x)
        listNxBFS.insert(1, y)
        x, y = test_Dijkstra(self, myGraph, nxGraph, 100)
        listMyDijkstra.insert(1, x)
        listNxDijkstra.insert(1, y)
        x, y = test_connected_components(self, myGraph, nxGraph)
        listMyConnected_components.insert(1, x)
        listNxConnected_components.insert(1, y)
        x = test_connected_component(self, myGraph, 100)
        listMyConnected_component.insert(1, x)

        myGraph.load_from_json("../data/G_1000_8000_1.json")
        nxGraph = load_networkX(self, "../data/G_1000_8000_1.json")

        x, y = test_shortPath(self, myGraph, nxGraph, 100)
        listMyShortPath.insert(2, x)
        listNxShortPath.insert(2, y)
        x, y = test_BFS(self, myGraph, nxGraph, 100)
        listMyBFS.insert(2, x)
        listNxBFS.insert(2, y)
        x, y = test_Dijkstra(self, myGraph, nxGraph, 100)
        listMyDijkstra.insert(2, x)
        listNxDijkstra.insert(2, y)
        x, y = test_connected_components(self, myGraph, nxGraph)
        listMyConnected_components.insert(2, x)
        listNxConnected_components.insert(2, y)
        x = test_connected_component(self, myGraph, 100)
        listMyConnected_component.insert(2, x)

        myGraph.load_from_json("../data/G_10000_80000_1.json")
        nxGraph = load_networkX(self, "../data/G_10000_80000_1.json")

        x, y = test_shortPath(self, myGraph, nxGraph, 100)
        listMyShortPath.insert(3, x)
        listNxShortPath.insert(3, y)
        x, y = test_BFS(self, myGraph, nxGraph, 100)
        listMyBFS.insert(3, x)
        listNxBFS.insert(3, y)
        x, y = test_Dijkstra(self, myGraph, nxGraph, 100)
        listMyDijkstra.insert(3, x)
        listNxDijkstra.insert(3, y)
        x, y = test_connected_components(self, myGraph, nxGraph)
        listMyConnected_components.insert(3, x)
        listNxConnected_components.insert(3, y)
        x = test_connected_component(self, myGraph, 100)
        listMyConnected_component.insert(3, x)

        myGraph.load_from_json("../data/G_20000_160000_1.json")
        nxGraph = load_networkX(self, "../data/G_20000_160000_1.json")

        x, y = test_shortPath(self, myGraph, nxGraph, 100)
        listMyShortPath.insert(4, x)
        listNxShortPath.insert(4, y)
        x, y = test_BFS(self, myGraph, nxGraph, 100)
        listMyBFS.insert(4, x)
        listNxBFS.insert(4, y)
        x, y = test_Dijkstra(self, myGraph, nxGraph, 100)
        listMyDijkstra.insert(4, x)
        listNxDijkstra.insert(4, y)
        x, y = test_connected_components(self, myGraph, nxGraph)
        listMyConnected_components.insert(4, x)
        listNxConnected_components.insert(4, y)
        x = test_connected_component(self, myGraph, 100)
        listMyConnected_component.insert(4, x)

        myGraph.load_from_json("../data/G_30000_240000_1.json")
        nxGraph = load_networkX(self, "../data/G_30000_240000_1.json")

        x, y = test_shortPath(self, myGraph, nxGraph, 100)
        listMyShortPath.insert(5, x)
        listNxShortPath.insert(5, y)
        x, y = test_BFS(self, myGraph, nxGraph, 100)
        listMyBFS.insert(5, x)
        listNxBFS.insert(5, y)
        x, y = test_Dijkstra(self, myGraph, nxGraph, 100)
        listMyDijkstra.insert(5, x)
        listNxDijkstra.insert(5, y)
        x, y = test_connected_components(self, myGraph, nxGraph)
        listMyConnected_components.insert(5, x)
        listNxConnected_components.insert(5, y)
        x = test_connected_component(self, myGraph, 100)
        listMyConnected_component.insert(5, x)

        print(listMyShortPath)
        print(listNxShortPath)
        print(listMyBFS)
        print(listNxBFS)
        print(listMyDijkstra)
        print(listNxDijkstra)
        print(listMyConnected_components)
        print(listNxConnected_components)
        print(listMyConnected_component)


def Graph_Comparisons(self: list, python_Comparisons: list, nx_Comparisons: list, func: str):
    x = ["Graph 1", "Graph 2", "Graph 3", "Graph 4", "Graph 5", "Graph 6"]
    plt.plot(x, self, label="java", color="blue")
    plt.plot(x, python_Comparisons, label="Python", color="black")
    plt.plot(x, nx_Comparisons, label="NetworkX", color="orange")
    plt.xlabel('Graphs')
    plt.ylabel('Average times in seconds')
    plt.title(func)
    plt.legend()
    plt.show()


def load_networkX(cls, fileName):
    graph = nx.DiGraph()
    edges_with_weights = []
    try:
        with open(fileName, "r") as file:
            dict = json.load(file)
            nodes = dict.get("Nodes")
            edges = dict.get("Edges")
            for node in nodes:
                graph.add_node(node.get("id"))
            for edge in edges:
                edge_data = (edge.get("src"), edge.get("dest"), edge.get("w"))
                edges_with_weights.append(edge_data)
            graph.add_weighted_edges_from(edges_with_weights)
            return graph
    except IOError as e:
        print(e)
        raise


def my_shortPath(graph: GraphAlgo, src: int, dest: int):
    startTime = time.perf_counter()
    print("The short path between", src, "to", dest, graph.shortest_path(src, dest))
    endTime = time.perf_counter()
    print("time", src, "to", dest, endTime - startTime)
    return endTime - startTime


def my_connected_component(graph: GraphAlgo, key: int):
    startTime = time.perf_counter()
    print("The connected_component of", key, "is", graph.connected_component(key))
    endTime = time.perf_counter()
    print("Time to find the connected_component of", key, "is", endTime - startTime)
    return endTime - startTime


def my_connected_components(graph: GraphAlgo):
    startTime = time.perf_counter()
    print(graph.connected_components())
    endTime = time.perf_counter()
    print("Time to find the connected_components in our project", endTime - startTime)
    return endTime - startTime


def my_dijkstra(graph: GraphAlgo, key: int):
    startTime = time.perf_counter()
    graph.Dijkstra(key)
    endTime = time.perf_counter()
    print("Time to run dijkstra of our project on node:", key, "is", endTime - startTime)
    return endTime - startTime


def my_BFS(graph: GraphAlgo, key: int):
    startTime = time.perf_counter()
    graph.BFS(key, True)
    endTime = time.perf_counter()
    print("Time to run BFS of our project on node:", key, "is", endTime - startTime)
    return endTime - startTime


def nx_shortPath(graph, src: int, dest: int):
    startTime = time.perf_counter()
    print("The short path between", src, "to", dest, nx.single_source_dijkstra(graph, src, dest))
    endTime = time.perf_counter()
    print("time", src, "to", dest, endTime - startTime)
    return endTime - startTime


def nx_connected_components(graph):
    startTime = time.perf_counter()
    print(nx.strongly_connected_components(graph))
    endTime = time.perf_counter()
    print("Time to find the connected_components in nx is", endTime - startTime)
    return endTime - startTime


def nx_dijkstra(graph, key: int):
    startTime = time.perf_counter()
    nx.single_source_dijkstra_path_length(graph, key)
    endTime = time.perf_counter()
    print("Time to run dijkstra of nx on node:", key, "is", endTime - startTime)
    return endTime - startTime


def nx_BFS(graph, key: int):
    startTime = time.perf_counter()
    nx.bfs_edges(graph, key)
    endTime = time.perf_counter()
    print("Time to run BFS of nx on node:", key, "is", endTime - startTime)
    return endTime - startTime


def test_shortPath(self, myGraph: GraphAlgo, nxGraph, numOfChecks: int):
    # shortest path
    myTotalTime = 0
    nxTotalTime = 0
    numOfNodesInGraph = len(myGraph.get_graph().get_all_v())
    i = 0
    while i < numOfChecks:
        src = random.randint(0, numOfNodesInGraph)
        dest = random.randint(0, numOfNodesInGraph)
        if myGraph.shortest_path(src, dest) != (float('inf'), []):
            myTotalTime += my_shortPath(myGraph, src, dest)
            nxTotalTime += nx_shortPath(nxGraph, src, dest)
            i += 1

    averageTimeMyShortPath = myTotalTime / numOfChecks
    print("my time:", averageTimeMyShortPath)
    averageTimeNXShortPath = nxTotalTime / numOfChecks
    print("nx time:", averageTimeNXShortPath)

    return averageTimeMyShortPath, averageTimeNXShortPath


def test_connected_components(self, myGraph: GraphAlgo, nxGraph):
    myTime = my_connected_components(myGraph)
    nxTime = nx_connected_components(nxGraph)

    return myTime, nxTime


def test_connected_component(self, myGraph: GraphAlgo, numOfChecks: int):
    numOfNodesInGraph = len(myGraph.get_graph().get_all_v())
    Time = 0
    i = 0
    while i < numOfChecks:
        key = random.randint(0, numOfNodesInGraph)
        Time += my_connected_component(myGraph, key)
        i += 1
    print("average time to run the function connected_component is:", Time / numOfChecks)
    return Time / numOfChecks


def test_BFS(self, myGraph: GraphAlgo, nxGraph, numOfChecks: int):
    # BFS algorithm
    myTotalTime = 0
    nxTotalTime = 0
    numOfNodesInGraph = len(myGraph.get_graph().get_all_v())
    nodes = myGraph.get_graph().get_all_v()

    i = 0
    while i < numOfChecks:
        key = random.randint(0, numOfNodesInGraph)
        if nodes.get(key) is not None:
            myTotalTime += my_BFS(myGraph, key)
            nxTotalTime += nx_BFS(nxGraph, key)
            i += 1
    averageTimeMyBFS = myTotalTime / numOfChecks
    print("my time:", averageTimeMyBFS)
    averageTimeNXBFS = nxTotalTime / numOfChecks
    print("nx time:", averageTimeNXBFS)

    return averageTimeMyBFS, averageTimeNXBFS


def test_Dijkstra(self, myGraph: GraphAlgo, nxGraph, numOfChecks: int):
    # Dijkstra algorithm
    myTotalTime = 0
    nxTotalTime = 0
    nodes = myGraph.get_graph().get_all_v()
    numOfNodesInGraph = len(myGraph.get_graph().get_all_v())
    i = 0
    while i < numOfChecks:
        key = random.randint(0, numOfNodesInGraph)
        if nodes.get(key) is not None:
            myTotalTime += my_dijkstra(myGraph, key)
            nxTotalTime += nx_dijkstra(nxGraph, key)
            i += 1
    averageTimeMyDijkstra = myTotalTime / numOfChecks
    print("my time:", averageTimeMyDijkstra)
    averageTimeNXDijkstra = nxTotalTime / numOfChecks
    print("nx time:", averageTimeNXDijkstra)

    return averageTimeMyDijkstra, averageTimeNXDijkstra
