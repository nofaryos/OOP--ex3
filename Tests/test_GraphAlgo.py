
from unittest import TestCase
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


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
        
        # load graph from file that not exist
        self.assertFalse(graph2.load_from_json("g"))

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
        # connected_component in graph without edges and without nodes
        list_empty = []
        graph = DiGraph()
        graphAlgo = GraphAlgo(graph)
        self.assertEqual(list_empty, graphAlgo.connected_component(0))

        # connected_component of node that do not exist in the graph
        graph.add_node(0)
        self.assertEqual(list_empty, graphAlgo.connected_component(1))
       
        # connected_component in graph without edges
        graph = createGraph(15)
        graphAlgo = GraphAlgo(graph)

        list_0 = [0]
        self.assertListEqual(list_0, graphAlgo.connected_component(0))

        # connected_component of node that do not exist in the graph

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
        # connected_components in graph without edges and without nodes
        list_empty = []
        graph = DiGraph()
        graphAlgo = GraphAlgo(graph)
        self.assertEqual(list_empty, graphAlgo.connected_component(0))  
        
        # graph with out edges
        graph = createGraph(6)
        graphAlgo = GraphAlgo(graph)

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


