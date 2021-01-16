import unittest
import json

from GraphAlgo import GraphAlgo
from DiGraph import DiGraph

class TestGraphAlgo(unittest.TestCase):

    def test_get_graph(self):
        graph_algo = GraphAlgo()
        graph = DiGraph()
        self.assertNotIsInstance(graph_algo.get_graph(), DiGraph)
        graph_algo.set_graph(graph)
        self.assertIsInstance(graph_algo.get_graph(), DiGraph)

    def test_load_from_json(self):
        t0_graph = DiGraph()
        for i in range(4):
            t0_graph.add_node(i)
        t0_graph.add_edge(0, 1, 1)
        t0_graph.add_edge(1, 0, 1.1)
        t0_graph.add_edge(1, 2, 1.3)
        t0_graph.add_edge(1, 3, 1.8)
        t0_graph.add_edge(2, 3, 1.1)
        graph_algo = GraphAlgo()
        graph_algo.load_from_json('../data/T0.json')
        self.assertEqual(t0_graph, graph_algo.get_graph())
    
    def test_save_to_json(self):
        name_of_src = '../data/T0.json'
        name_of_saved = '../data/T0_TEST.json'
        graph_algo = GraphAlgo()
        graph_algo.load_from_json(name_of_src)
        graph_algo.save_to_json(name_of_saved)
        try:
            src = open(name_of_src, 'r')
            saved = open(name_of_saved, 'r')
            src_json = json.load(src)
            saved_json = json.load(saved)
            src.close()
            saved.close()
            src = json.dumps(src, sort_keys=True)
            saved = json.dumps(saved, sort_keys=True)
            self.assertEqual(src, saved)
        except:
            pass
    
    def test_shortest_path(self):
        no_path = (float('inf'), [])
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        self.assertEqual(no_path, graph_algo.shortest_path(0, 1))
        self.assertEqual(no_path, graph_algo.shortest_path(2, 3))
        self.assertEqual(no_path, graph_algo.shortest_path(1, 3))
        for i in range(4):
            graph.add_node(i)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 0.5)
        graph.add_edge(0, 2, 4.5)
        graph.add_edge(2, 3, 1)
        graph.add_edge(0, 3, 8)
        self.assertEqual((2.5, [0, 1, 2, 3]), graph_algo.shortest_path(0, 3))
        self.assertEqual((1.5, [0, 1, 2]), graph_algo.shortest_path(0, 2))
        graph.add_edge(1, 3, 1.4)
        self.assertEqual((2.4, [0, 1, 3]), graph_algo.shortest_path(0, 3))
        self.assertEqual(no_path, graph_algo.shortest_path(2, 4))

    def test_connected_component_and_components(self):
        graph = DiGraph()
        graph_algo = GraphAlgo(graph)
        for i in range(5):
            graph.add_node(i)
        graph.add_edge(0, 1, 1)
        graph.add_edge(1, 2, 1)
        graph.add_edge(2, 3, 1)
        graph.add_edge(3, 0, 1)
        self.assertEqual(0, len(graph_algo.connected_component(6)))
        self.assertEqual(1, len(graph_algo.connected_component(4)))
        for i in range(4):
            is_in_scc = any(i == node.get_node_id() for node in graph_algo.connected_component(1))
            self.assertTrue(is_in_scc)
        
        components_list =  graph_algo.connected_components()
        self.assertEqual(2, len(components_list))
        self.assertTrue(components_list[1][0].get_node_id() == 4)

    def test_plot_graph(self):
        name_of_src = '../data/A1'
        graph_algo = GraphAlgo()
        graph_algo.load_from_json(name_of_src)
        graph_algo.plot_graph()

    
if __name__ == '__main__':
    unittest.main()