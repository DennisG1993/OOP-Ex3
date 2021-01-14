from GraphInterface import GraphInterface
from NodeData import NodeData

class DiGraph(GraphInterface):
    def __init__(self):
        self.nodes: Dict[int, NodeData] = {}
        self.edges: Dict[int, Dict[int, float]] = {}
        self.edges_of_node: Dict[int, Dict[int, float]] = {}
        self.mc: int = 0
        self.num_of_edges: int = 0

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        return self.num_of_edges

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.edges_of_node.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.edges.get(id1)

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        #Adds an edge to the graph return true if succeded else false and does nothing
        node1 = self.nodes.get(id1)
        node2 = self.nodes.get(id2)
        nodes_exist = node1 is not None and node2 is not None

        if weight >= 0 and id1 != id2 and nodes_exist:
            id2_edges = self.edges_of_node.get(id2)
            opposite_edge = id2_edges.get(id1)
            id1_edges = self.edges.get(id1)

            if opposite_edge is None:
                self.num_of_edges += 1
            elif id1_edges.get(id2) == weight:
                return True

            self.mc += 1
            id1_edges[id2] = weight
            id2_edges[id1] = weight
            return True

        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        node_not_in_graph = self.nodes.get(node_id) is None
        if node_not_in_graph:
            node = NodeData(node_id, pos)
            self.nodes[node_id] =  node
            self.edges[node_id] = {}
            self.edges_of_node[node_id] = {}
            self.mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
       # Removes a node from the graph and returns true if it succeded else do nothing and return false
        node_exists = self.nodes.get(node_id) is not None
        if node_exists:
            initial_in_edges = self.all_in_edges_of_node(node_id).copy() # since we are removing edges we use copy to get inital state
            for edge in initial_in_edges:
                self.remove_edge(edge, node_id)
                self.mc -= 1 #added cause of the last requirement that remove node will only change mc by 1
            self.edges_of_node.pop(node_id)
            initial_out_edges = self.all_out_edges_of_node(node_id).copy() # since we are removing edges we use copy to get inital state
            for edge in initial_out_edges:
                self.remove_edge(node_id, edge)
                self.mc -= 1 #added cause of the last requirement that remove node will only change mc by 1
            self.edges.pop(node_id)
            self.nodes.pop(node_id)
            self.mc += 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        #Removes an edge from the graph and returns true if succeded else does nothing and returns false
        edges = self.edges.get(node_id1)
        edges_exist = edges is not None
        if edges_exist:
            edge_exist = edges.get(node_id2) is not None
            if edge_exist:
                edges.pop(node_id2)
                self.edges_of_node.get(node_id2).pop(node_id1)
                self.mc += 1
                self.num_of_edges -= 1
                return True
        return False

    def __repr__(self):
        edges = []
        for edge in self.edges.values():
            for e in edge.values():
                edges.append(e)
        return f"""{{
    Nodes: {str(list(self.nodes.values()))},
    Edges: {str(edges)}
}}"""

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        is_node_equal = self.nodes == other.nodes
        is_edges_equal = self.edges == other.edges
        return is_node_equal and is_edges_equal