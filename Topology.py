import networkx as nx
import math
import json


class _Topology():
    def __init__(self, nodes, edges):
        self.graph = nx.Graph()
        for n in nodes:
            self.graph.add_node(nodes[n][0], lon=nodes[n][1], lat=nodes[n][2], pos=(nodes[n][1], nodes[n][2]),
                                num_of_IXPs=nodes[n][3],
                                num_of_DCs=nodes[n][4])
        for e in edges:
            self.graph.add_edge(edges[e]['startNode'], edges[e]['endNode'], linkDist=round(edges[e]['linkDist'],2),
                                noChannels=edges[e]['noChannels'], noSpans=edges[e]['noSpans'],
                                spanList=edges[e]['spanList'],
                                capacity=4400, available_slots=list(range(0, 352)), used_slots=[], used_capacity=0)
        self.avg_nodal_degree = self._calc_degree()
        self.traffic = self._cal_traffic_matrix()
        #self.traffic_demand=self._cal_traffic_demand()
        self.traffic_demand = self._cal_traffic_demand_from_file()
        self.paths = self._cal_k_shortest_paths()


    def _calc_degree(self):
        degree = 0
        for node in self.graph.nodes():
            degree = degree + self.graph.degree(node)
        return degree / self.graph.number_of_nodes()

    def _cal_traffic_matrix(self):
        traffic = {}
        for i in self.graph.nodes:
            for j in self.graph.nodes:
                if (i == j):
                    traffic[i, j] = 0
                    # traffic[(i,j)] = 0

                else:
                    combined_node_degree = self.graph.degree(i) + self.graph.degree(j)
                    del_i = self.graph.nodes[i]["num_of_IXPs"] - self.graph.nodes[i]["num_of_DCs"]
                    del_j = self.graph.nodes[j]["num_of_IXPs"] - self.graph.nodes[j]["num_of_DCs"]
                    if (combined_node_degree > 2 * self.avg_nodal_degree):
                        bin_coff = (math.factorial(combined_node_degree)) / (
                                math.factorial(2) * math.factorial(combined_node_degree - 2))
                        # traffic[(i,j)] =  2*bin_coff*del_i*del_j
                        traffic[i, j] = 2 * bin_coff * del_i * del_j
                    else:
                        # traffic[(i,j)] = combined_node_degree*del_i*del_j
                        traffic[i, j] = combined_node_degree * del_i * del_j

        return traffic
    def _cal_traffic_demand(self):
        traffic_matrix = self.traffic.copy()
        for i in self.traffic:
            if i in traffic_matrix.keys():
                j=(i[1],i[0])
                traffic_matrix.pop(j)
        print("Total Traffic Demand {}".format(len(traffic_matrix)))
        return traffic_matrix

    def _cal_traffic_demand_from_file(self):
        traffic_demand = {}
        with open(
                "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Demands_Germany_17_init_traff.json") as demand_file:
            demands = json.load(demand_file)
        for i in demands:
            traffic_demand[(demands[i][0], demands[i][1])] = demands[i][2]
        return traffic_demand


    def _cal_k_shortest_paths(self):
        paths = {}
        links = {}
        for i in self.traffic_demand.items():
            if i[1] > 0:
                # s_paths = nx.shortest_simple_paths(self.graph, source=i[0][0], target=i[0][1], weight='linkDist')#
                s_paths = nx.node_disjoint_paths(self.graph, s=i[0][0], t=i[0][1], cutoff=2)
                for s_path in s_paths:
                    link_dist = self._cal_path_length(s_path)
                    links[link_dist] = s_path

                for x in range(0, len(list(links.keys()))):
                    # Find the shortest path
                    if list(links.keys())[x] <= min(key1 for key1 in links.keys()):
                        paths[i[0][0], i[0][1], 0] = [list(links.values())[x], list(links.keys())[x]]
                    else:
                        paths[i[0][0], i[0][1], 1] = [list(links.values())[x], list(links.keys())[x]]
                links.clear()

                #
                # for x in range(0,2):
                #
                #
                #     paths[i[0][0], i[0][1], 0] = [path, self._cal_path_length(path)]
                #
                #     print(path)
                #     paths[i[0][0],i[0][1],x] = [path, self._cal_path_length(path)]


        return paths

    def _cal_path_length(self, path):
        link_distance = 0
        pairs = [path[i: i + 2] for i in range(len(path) - 1)]
        for link in pairs:
            link_distance = link_distance + self.graph[link[0]][link[1]]['linkDist']
        return link_distance

    # def _calc_paths(self):
