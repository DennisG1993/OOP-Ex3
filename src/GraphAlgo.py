from typing import List, Dict
import json

from DiGraph import DiGraph
from NodeData import NodeData
from GraphInterface import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface

class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph: GraphInterface = None):
        super()
        self.graph = graph
        self.scc_set = set();
        self.scc_list = []
        self.index_for_conectivity = 0
        self.smallest_reachable = {}
        self.visited = {}

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        #this method recives relative file path as file_name and attemps to open read it and create a grah from it.
        #returns true on successs otherwise returns false
        graph = DiGraph()
        try:
            file = open(file_name, 'r')
            graph_json = json.load(file)
            for node in graph_json['Nodes']:
                id = node['id']
                pos = None
                if 'pos' in node:
                    pos = tuple([float(cord) for cord in node['pos'].split(',')])
                graph.add_node(id, pos)

            for edge in graph_json['Edges']:
                edge_src = edge['src']
                edge_dest = edge['dest']
                weight = edge['w']
                graph.add_edge(edge_src, edge_dest, weight)

            self.graph = graph
            file.close()
            return True
        except:
            return False

    def save_to_json(self, file_name: str) -> bool:
        #this method recives relative file path as file_name and attemps write a graph to it.
        #if file in that path exists it will be over written else will be created
        #returns true on successs otherwise returns false
        try:
            file = open(file_name, 'w')
            nodes = self.graph.get_all_v()
            nodes_list = [node.to_dict() for node in nodes.values()]
            edges = [{'src': node_id, 'dest': int(dest), 'w': w} for node_id in nodes for dest, w in self.graph.all_out_edges_of_node(node_id).items()]
            json.dump({'Nodes': nodes_list, 'Edges': edges}, file)
            file.close()
            return True
        except Exception as e:
            return False



    def shortest_path(self, id1: int, id2: int) -> (float, list):
        #implemented shortest path algorithm using dijkstra
        queue = []
        visited = set()
        dist = {}
        prev = {}
        for v in self.graph.get_all_v():
            dist[v] = float('inf')
            prev[v] = None
        dist[id1] = 0
        queue.append((id1, dist[id1]))
        while len(queue) and len(visited) != self.graph.v_size():
            id_weight_tuple = min(queue, key=lambda x: x[1])
            queue.remove(id_weight_tuple)
            if id_weight_tuple not in visited:
                visited.add(id_weight_tuple[0])
                if id_weight_tuple[0] == id2:
                    if prev[id2] is not None or id2 == id1:
                        path_id = id2
                        path = []
                        while path_id is not None:
                            path.insert(0, path_id)
                            path_id = prev[path_id]
                        return dist[id2], path
                connected_nodes = self.graph.all_out_edges_of_node(id_weight_tuple[0]).items()
                for neighbor_node_id, w in connected_nodes:
                    if neighbor_node_id not in visited and dist[id_weight_tuple[0]] + w < dist[neighbor_node_id]:
                        dist[neighbor_node_id] = dist[id_weight_tuple[0]] + w
                        prev[neighbor_node_id] = id_weight_tuple[0]
                        queue.append((neighbor_node_id, dist[neighbor_node_id]))

        return dist[id2], []


    def trajan_algorithm(self, node_id):
        #kind of implementation of trajan algorithm some parts of it were found on the internet in psudo code and implemented in python for our needs
        stack = [node_id]
        scc: Dict[int, list] = {}
        nodes = self.graph.get_all_v()
        while stack:
            node = stack[-1]
            if node not in self.visited:
                self.visited[node] =  self.index_for_conectivity
                self.smallest_reachable[node] = self.index_for_conectivity
                scc[self.index_for_conectivity] = [nodes[node]]
                self.index_for_conectivity += 1
            did_visit_all = True
            connected_nodes = self.graph.all_out_edges_of_node(node)
            for dest in connected_nodes:
                if dest not in self.visited:
                    stack.append(dest)
                    did_visit_all = False
                    break
            if did_visit_all:
                low = self.smallest_reachable[node]
                for dest in connected_nodes:
                    if dest not in self.scc_set:
                        self.smallest_reachable[node] = min(self.smallest_reachable[node], self.smallest_reachable[dest])
                stack.pop()
                if self.smallest_reachable[node] == self.visited[node]:
                    self.scc_list.append(scc[self.smallest_reachable[node]])
                    ids_list = [node.get_node_id() for node in scc[self.smallest_reachable[node]]]
                    self.scc_set.update(ids_list)
                else:
                    if self.smallest_reachable[node] not in scc:
                        scc[self.smallest_reachable[node]] = [node]
                    scc[self.smallest_reachable[node]].extend(scc[low])
                    for key in scc[low]:
                        self.smallest_reachable[key.get_node_id()] = self.smallest_reachable[node]
         

    def connected_component(self, id1: int) -> list:
        self.reset_for_conectivity_algo()
        self.trajan_algorithm(id1)
        for scc in self.scc_list:
            node_ids_list = [node.get_node_id() for node in scc]
            if id1 in node_ids_list:
                return scc

    def connected_components(self) -> List[list]:
        self.reset_for_conectivity_algo()
        
        for node_id in self.graph.get_all_v():
            if node_id not in self.scc_set:
                self.trajan_algorithm(node_id)
        return self.scc_list

    def plot_graph(self) -> None:
        #sadly i didnt have the time to implement this method
        #hopefully we will be able to hand the assignment a day or two later so i can implement it
        pass

    def reset_for_conectivity_algo(self):
        self.scc_set = set()
        self.scc_list = []
        self.index_for_conectivity = 0
        self.smallest_reachable = {}
        self.visited = {}