from unittest import TestCase

from DiGraph import DiGraph


# function for creating graph
def createGraph(n):
    graph = DiGraph()
    for i in range(n):
        graph.add_node(i)
    return graph


class TestDiGraph(TestCase):

    def test_v_size(self):
        graph = createGraph(10)
        # graph with 10 nodes
        self.assertEqual(10, graph.v_size())
        for i in range(10):
            graph.remove_node(i)
        # empty graph
        self.assertEqual(0, graph.v_size())
        graph.add_node(0)
        # graph with 1 node
        self.assertEqual(1, graph.v_size())
        # Adding node that already exist in the graph
        graph.add_node(0)
        self.assertEqual(1, graph.v_size())

    def test_e_size(self):
        graph = createGraph(20)
        self.assertEqual(0, graph.e_size())
        for i in range(20):
            graph.add_edge(0, i, 2)
        self.assertEqual(19, graph.e_size())
        # Adding an edge between node to itself.
        graph.remove_edge(0, 0)
        self.assertEqual(19, graph.e_size())
        graph.remove_edge(0, 1)
        self.assertEqual(18, graph.e_size())
        graph.remove_node(0)
        self.assertEqual(0, graph.e_size())

    def test_get_all_v(self):
        graph = createGraph(0)
        a = DiGraph.nodeData(0)
        b = DiGraph.nodeData(1)
        c = DiGraph.nodeData(2)
        d = DiGraph.nodeData(3)
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        result = {0: a, 1: b, 2: c, 3: d}
        self.assertDictEqual(result, graph.get_all_v())

    def test_all_in_edges_of_node(self):
        graph = createGraph(15)
        graph1 = {}
        # node that not exist in the graph
        self.assertIsNone(graph.all_in_edges_of_node(20))

        # node that exist in the graph but without in edges
        self.assertEqual(graph1, graph.all_in_edges_of_node(1))
        
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 4, 0)
        graph.add_edge(4, 5, 2)
        self.assertDictEqual(graph1, graph.all_in_edges_of_node(3))
        graph.add_edge(4, 3, 2)
        graph.add_edge(4, 10, 4.5)
        self.assertIsNotNone(graph.all_in_edges_of_node(4))
        graph.remove_node(4)
        self.assertIsNone(graph.all_in_edges_of_node(4))
        self.assertIsNotNone(graph.all_in_edges_of_node(3))
        graph.remove_edge(2, 4)
        self.assertIsNone(graph.all_in_edges_of_node(4))

    def test_all_out_edges_of_node(self):
        graph = createGraph(15)
        graph1 = {}
        
        # node that not exist in the graph
        self.assertIsNone(graph.all_out_edges_of_node(20))

        # node that exist in the graph but without out edges
        self.assertEqual(graph1, graph.all_out_edges_of_node(1))
        
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 3, 0)
        graph.add_edge(4, 6, 2)
        self.assertDictEqual(graph1, graph.all_out_edges_of_node(3))
        graph.add_edge(3, 2, 2)
        graph.add_edge(3, 5, 2)
        graph.add_edge(4, 5, 1)
        self.assertEqual(2, len(graph.all_out_edges_of_node(3)))
        graph.remove_node(3)
        self.assertIsNone(graph.all_out_edges_of_node(3))
        graph.add_edge(2, 10, 1)
        self.assertIsNotNone(graph.all_out_edges_of_node(2))
        graph.remove_edge(4, 6)
        graph.remove_edge(4, 5)
        self.assertEqual(graph1, graph.all_out_edges_of_node(4))

    def test_get_mc(self):
        graph = createGraph(20)
        self.assertEqual(20, graph.get_mc())
        for i in range(20):
            graph.add_edge(0, i, 2)
        self.assertEqual(39, graph.get_mc())
        graph.remove_edge(0, 0)
        self.assertEqual(39, graph.get_mc())
        graph.remove_edge(0, 1)
        self.assertEqual(40, graph.get_mc())
        graph.remove_node(0)
        self.assertEqual(41, graph.get_mc())

    def test_add_edge(self):
        graph = createGraph(30)
        for i in range(30):
            graph.add_edge(0, i, i + 2)
        # Check that we are not connect between node to itself
        self.assertIsNone(graph.all_out_edges_of_node(0).get(0))
        # Check that we are able to connect between nodes in the graph
        self.assertEqual(6, graph.all_out_edges_of_node(0).get(4))
        self.assertIsNone(graph.all_out_edges_of_node(4).get(0))
        graph.add_edge(4, 0, 2)
        self.assertEqual(2, graph.all_out_edges_of_node(4).get(0))
        graph.add_edge(0, 2, -5)
        self.assertEqual(4, graph.all_out_edges_of_node(0).get(2))

    def test_add_node(self):
        graph = createGraph(10)
        graph.add_node(15)
        self.assertEqual(11, graph.v_size())
        # Check that we are able to add node to the graph
        self.assertIsNotNone(graph.get_all_v().get(15))
        self.assertIsNone(graph.get_all_v().get(10))
        graph.remove_node(0)
        self.assertIsNone(graph.get_all_v().get(0))
        graph.add_node(0)
        self.assertIsNotNone(graph.get_all_v().get(0))

    def test_remove_node(self):
        graph = createGraph(30)
        r = graph.v_size()
        for i in range(r):
            graph.add_edge(0, i, i)
            graph.add_edge(i, 0, i)
        # Check that we are able to remove node from the graph
        graph.remove_node(0)
        self.assertIsNone(graph.all_out_edges_of_node(2).get(0))
        self.assertIsNone(graph.all_in_edges_of_node(2).get(0))
        self.assertIsNone(graph.all_in_edges_of_node(1).get(0))
        self.assertIsNone(graph.all_out_edges_of_node(1).get(0))
        self.assertIsNone(graph.all_in_edges_of_node(40))
        self.assertIsNone(graph.all_out_edges_of_node(0))
        self.assertIsNone(graph.get_all_v().get(0))
        self.assertEqual(0, graph.e_size())
        self.assertEqual(29, graph.v_size())

    def test_remove_edge(self):
        graph = createGraph(15)
        graph.add_edge(1, 2, 3.14)
        graph.add_edge(3, 4, 0)
        graph.add_edge(4, 5, 2)
        graph.add_edge(6, 10, 4.5)
        graph.add_edge(5, 10, 1)
        self.assertIsNotNone(graph.all_out_edges_of_node(6))
        self.assertEqual(4.5, graph.outEdges.get(6).get(10))
        # Check that we are able to remove edge from the graph
        graph.remove_edge(4, 5)
        self.assertIsNone(graph.all_out_edges_of_node(4).get(5))
        self.assertFalse(graph.remove_edge(7, 8))
        self.assertNotEqual(3, graph.outEdges.get(1).get(2))
