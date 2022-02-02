import json
import math

import matplotlib.pyplot as plt
import networkx as nx

import CTModelling as ct
import Modulation
from Topology import _Topology

with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Nodes_Germany_17.json") as node_file:
    nodes = json.load(node_file)
with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Links_Germany_17.json") as edge_file:
    edges = json.load(edge_file)


class RMSA():
    def __init__(self):
        self.topology = _Topology(nodes, edges)
        self.links = self.topology.paths
        self.traffic = self.topology.traffic_demand
        self.regen = len(nodes)
        #self.ctmodel = ct.Msg_Modelling()

    def _check_continuity(self, list1, list2):
        for li in list1:
            if all(x in li for x in list2):
                check_continuity = True
                continue
            else:
                check_continuity = False
                break
        return check_continuity

    def _cal_possible_connections(self, available_slots, slots, pairs):
        blocked = True
        common_items = set.intersection(*map(set, available_slots))
        common_slots = list(common_items)

        ranges = sum((list(t) for t in zip(common_slots, common_slots[1:]) if t[0] + 1 != t[1]), [])
        iranges = iter(common_slots[0:1] + ranges + common_slots[-1:])
        continuity = False
        if iranges:
            for n in iranges:
                initial_slot = n
                end_slot = next(iranges)
                required_slots_last_index = (initial_slot + slots) - 1

                if (required_slots_last_index) > end_slot:
                    # print("proper slots not found")
                    continuity = False
                    continue
                else:
                    candidate_slots = [x for x in range(initial_slot, required_slots_last_index + 1)]
                    # print("proper slots  found {}".format(candidate_slots))
                    continuity = True
                    break

        if continuity:
            for edges in pairs:
                self.topology.graph[edges[0]][edges[1]]['available_slots'] = [item for item in
                                                                         self.topology.graph[edges[0]][edges[1]][
                                                                             'available_slots'] if
                                                                         item not in candidate_slots]
                self.topology.graph[edges[0]][edges[1]]['used_slots'].extend(candidate_slots)
                self.topology.graph[edges[0]][edges[1]]['used_capacity'] = len(
                    self.topology.graph[edges[0]][edges[1]]['used_slots'])
            blocked = False
        return blocked

    def _calculate_bvt(self, bitrate, max_capacity):
        bvt_one_end = math.ceil(bitrate / max_capacity)
        return  bvt_one_end

    def _cal_spectral_assignment(self, link, demand):
        pairs = [link[0][i: i + 2] for i in range(len(link[0]) - 1)]
        edge_length = []
        list_of_avail_slots = []
        for p in pairs:
            edge_length.append(self.topology.graph[p[0]][p[1]]['linkDist'])
            list_of_avail_slots.append(self.topology.graph[p[0]][p[1]]['available_slots'])
        # print('Max distance {}'.format(max(edge_length)))

        slots, mod_type, max_capacity = Modulation._select_modulation(link_distance=max(edge_length),
                                                                           bitrate=demand)
        edge_length.clear()

        blocked = self._cal_possible_connections(list_of_avail_slots, slots, pairs)
        bvt = 2*(self._calculate_bvt(demand,max_capacity) * len(link[0]))-2
        # print("list_of_avail_slots {}".format(list_of_avail_slots))
        list_of_avail_slots.clear()
        return blocked, bvt, mod_type

    def execute_RMSA(self):
        accepted_connections = {}
        blocked_connections = []
        transponders = 0

        blocked = True
        ## For visualizing the graph
       # pos = nx.get_node_attributes(self.topology.graph, 'pos')
        pos= nx.spring_layout(self.topology.graph)
        #pos=nx.random_layout(topology.graph, seed=14)
        #pos = nx.nx_agraph.graphviz_layout(topology.graph)
        #labels = nx.get_edge_attributes(self.topology.graph, 'linkDist')
        nx.draw(self.topology.graph, pos, with_labels=True,node_color='skyblue', node_size=220, font_size=8, font_weight="bold")
        #nx.draw_networkx_edge_labels(self.topology.graph,pos)
        plt.savefig("TopologyVisual.png")
        plt.clf()
        for i in self.traffic:
            print("traffic {}".format(i))
            if self.traffic[i] > 0:
                blocked = True
                for j in range(0, 2):
                    # choose shortest path first
                    link = self.links[i[0], i[1], j]
                    isBlocked, bvt, mod_type = self._cal_spectral_assignment(link, self.traffic[i])
                    if not isBlocked:
                        print('link {}'.format(link))
                        blocked = False
                        accepted_connections[i] = [link, mod_type, bvt, self.traffic[i]]
                        transponders = transponders + bvt
                        break

                if blocked:
                    blocked_connections.append(i)

        # print("All Blocked Connections are: {}".format(blocked_connections))
        # print("All Accepted connections are: \n")
        # for a in accepted_connections:
        #     print("{}\n".format(accepted_connections[a]))
        # print("All Accepted connections are {}".format(accepted_connections))
        print("Total number of Roadms {}".format(self.regen))
        print("Total number of transponders {}".format(transponders))
        # pos = nx.get_node_attributes(self.topology.graph, 'pos')
        # pos = nx.spring_layout(self.topology.graph)
        # # pos=nx.random_layout(topology.graph, seed=13)
        # labels = nx.get_edge_attributes(self.topology.graph, 'used_capacity')
        # nx.draw(self.topology.graph, pos, with_labels=True, node_color='skyblue', node_size=220, font_size=8,
        #         font_weight="bold")
        # nx.draw_networkx_edge_labels(self.topology.graph, pos, edge_labels=labels)
        # plt.savefig("TopologyVisual_Connected.png")
        # plt.clf()
        return accepted_connections, blocked_connections, self.regen, transponders


