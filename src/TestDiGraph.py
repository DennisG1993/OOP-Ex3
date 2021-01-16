import unittest

from DiGraph import DiGraph

class DiGraphTests(unittest.TestCase):

    # test case function to check the DiGraph.v_size function
    def test_v_size(self):
        nodes_to_add = 30
        graph = DiGraph()
        for i in range(nodes_to_add):
            graph.add_node(i)
        self.assertEqual(nodes_to_add, graph.v_size())
        for i in range(0, 30, 2):
            graph.remove_node(i)
        self.assertEqual(15, graph.v_size())
        graph.remove_node(0)
        graph.remove_node(2)
        self.assertEqual(15, graph.v_size())
        
    # test case function to check the DiGraph.e_size function
    def test_e_size(self):
        nodes_to_add = 50
        half = 25
        graph = DiGraph()
        after_first_addition = 25 * 25
        self.assertEqual(0, graph.e_size())
        for i in range(nodes_to_add):
            graph.add_node(i)
        for i in range(half):
            for j in range(half, nodes_to_add):
                graph.add_edge(i, j, 1)
        self.assertEqual(after_first_addition, graph.e_size())
        graph.add_edge(0, 25, 1)
        graph.add_edge(1, 26, 1)
        graph.add_edge(0, 1, 1)
        self.assertEqual(after_first_addition + 1, graph.e_size())
        graph.remove_edge(0, 7)
        self.assertEqual(after_first_addition + 1, graph.e_size())
        graph.remove_edge(0, 27)
        self.assertEqual(after_first_addition, graph.e_size())

    def test_get_all_v(self):
        nodes_to_add = 30
        graph = DiGraph()
        for i in range(nodes_to_add):
            graph.add_node(i)
        
        for i in range(nodes_to_add):
           self.assertIsNone(graph.get_all_v().get(nodes_to_add + i))
           self.assertIsNotNone(graph.get_all_v().get(i))
        self.assertEqual(nodes_to_add, len(graph.get_all_v()))


    def test_all_in_edges_of_node(self):
        nodes_to_add = 50
        half = 25
        graph = DiGraph()
        after_first_addition = 25 * 25
        self.assertEqual(0, graph.e_size())
        for i in range(nodes_to_add):
            graph.add_node(i)
        for i in range(half):
            for j in range(half, nodes_to_add):
                graph.add_edge(i, j, j)
        for i in range(half):
            in_edges = graph.all_in_edges_of_node(i)
            in_edges_second_half = graph.all_in_edges_of_node(i + 25)
            self.assertEqual(len(in_edges), 0)
            self.assertEqual(len(in_edges_second_half), 25)

    def test_all_out_edges_of_node(self):
        nodes_to_add = 50
        half = 25
        graph = DiGraph()
        after_first_addition = 25 * 25
        self.assertEqual(0, graph.e_size())
        for i in range(nodes_to_add):
            graph.add_node(i)
        for i in range(half):
            for j in range(half, nodes_to_add):
                graph.add_edge(i, j, j)
        for i in range(half):
            out_edges = graph.all_out_edges_of_node(i)
            out_edges_second_half = graph.all_out_edges_of_node(i + 25)
            self.assertEqual(len(out_edges), 25)
            self.assertEqual(len(out_edges_second_half), 0)
    
    def test_get_mc(self):
        nodes_to_add = 50
        half = 25
        graph = DiGraph()
        after_first_addition = 25 * 25
        self.assertEqual(0, graph.e_size())
        for i in range(nodes_to_add):
            graph.add_node(i)
        self.assertEqual(graph.get_mc(), nodes_to_add)
        for i in range(half):
            for j in range(half, nodes_to_add):
                graph.add_edge(i, j, 1)

        self.assertEqual(graph.get_mc(), 675)
        graph.remove_node(1)
        self.assertEqual(graph.get_mc(), 676)

    def test_add_edge(self):
        nodes_to_add = 50
        half = 25
        graph = DiGraph()
        after_first_addition = 25 * 25
        self.assertEqual(0, graph.e_size())
        for i in range(nodes_to_add):
            graph.add_node(i)
        for i in range(half):
            for j in range(half, nodes_to_add):
                self.assertTrue(graph.add_edge(i, j, 1))
        self.assertFalse(graph.add_edge(60, 1, 1))
        self.assertFalse(graph.add_edge(0, 5, -1))
        

    def test_add_node(self):
        nodes_to_add = 50
        half = 25
        graph = DiGraph()
        for i in range(nodes_to_add):
            self.assertTrue(graph.add_node(i, (i, i*i, i*i*i)))
            self.assertFalse(graph.add_node(i))

    
    def test_remove_node(self):
        nodes_to_add = 50
        half = 25
        graph = DiGraph()
        for i in range(nodes_to_add):
            graph.add_node(i)
            self.assertTrue(graph.remove_node(i))
            self.assertFalse(graph.remove_node(i))
        




if __name__ == '__main__':
    unittest.main()