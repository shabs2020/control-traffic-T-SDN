from Topology import _Topology
import json
import math

import Modulation
import matplotlib.pyplot as plt

import networkx as nx

with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Nodes_Germany_17.json") as node_file:
    nodes = json.load(node_file)
with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Links_Germany_17.json") as edge_file:
    edges = json.load(edge_file)

topology = _Topology(nodes, edges)
regen = len(nodes)
links = topology.paths

# print("Total two disjoin paths {}".format(links))
paths = []
for l in links:

    if l[2] == 0:

        paths.append(links[l])
traffic = topology.traffic
print("total Paths found {}".format(len(paths)))
print("trffaic marix size{}".format(len(traffic)))
symmetric_traffic = topology.traffic_demand
# print("trafficdemand {}".format(traffic))


def _check_continuity(list1, list2):
    for li in list1:
        if all(x in li for x in list2):
            check_continuity = True
            continue
        else:
            check_continuity = False
            break
    return check_continuity


def _cal_possible_connections(available_slots, slots, pairs):
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
                #print("proper slots not found")
                continuity = False
                continue
            else:
                candidate_slots = [x for x in range(initial_slot, required_slots_last_index + 1)]
                #print("proper slots  found {}".format(candidate_slots))
                continuity = True
                break

    if continuity:
        for edges in pairs:
            topology.graph[edges[0]][edges[1]]['available_slots'] = [item for item in
                                                                     topology.graph[edges[0]][edges[1]][
                                                                         'available_slots'] if
                                                                     item not in candidate_slots]
            topology.graph[edges[0]][edges[1]]['used_slots'].extend(candidate_slots)
            topology.graph[edges[0]][edges[1]]['used_capacity'] = len(
                topology.graph[edges[0]][edges[1]]['used_slots'])
        blocked=False
    # if iranges:
    #     for n in iranges:
    #         initial_slot = n
    #         end_slot = next(iranges)
    #         required_slots_last_index = (initial_slot + slots) - 1
    #
    #         if (required_slots_last_index) > end_slot:
    #             continue
    #         else:
    #             candidate_slots = [x for x in range(initial_slot, required_slots_last_index + 1)]
    #             all_available_slots = [topology.graph[edges[0]][edges[1]]['available_slots'] for edges in pairs]
    #             continuity = _check_continuity(all_available_slots, candidate_slots)
    #             if continuity:
    #                 for edges in pairs:
    #                     topology.graph[edges[0]][edges[1]]['available_slots'] = [item for item in
    #                                                                              topology.graph[edges[0]][edges[1]][
    #                                                                                  'available_slots'] if
    #                                                                              item not in candidate_slots]
    #                     topology.graph[edges[0]][edges[1]]['used_slots'].extend(candidate_slots)
    #                     topology.graph[edges[0]][edges[1]]['used_capacity'] = len(
    #                         topology.graph[edges[0]][edges[1]]['used_slots'])
    #                     #
    #                     # print("Used Slots: {}".format(topology.graph[edges[0]][edges[1]]['used_slots']))
    #                     # with open("UsedSlots.txt", "a") as myfile:
    #                     #     myfile.write(str(edges) + ':' + str(topology.graph[edges[0]][edges[1]]['used_slots'])+"\n")
    #                     # myfile.close()
    #                     # with open("AvailableSlots.txt", "a") as myfile:
    #                     #     myfile.write(str(edges) + ':' + str(topology.graph[edges[0]][edges[1]]['available_slots'])+"\n")
    #                     # myfile.close()
    #
    #                     # print("Available Slots are {}".format(topology.graph[edges[0]][edges[1]]['available_slots']))
    #                     # print("Used Capacity {}".format(topology.graph[edges[0]][edges[1]]['used_capacity']))
    #                 blocked = False
    #                 break
    return blocked




def _cal_spectral_assignment(link, demand):
    pairs = [link[0][i: i + 2] for i in range(len(link[0]) - 1)]
    edge_length = []
    list_of_avail_slots=[]



    for p in pairs:
        edge_length.append(topology.graph[p[0]][p[1]]['linkDist'])
        list_of_avail_slots.append(topology.graph[p[0]][p[1]]['available_slots'])
    # print('Max distance {}'.format(max(edge_length)))

    bvt, slots, mod_type, max_capacity = Modulation._select_modulation(link_distance=max(edge_length), bitrate=demand)
    edge_length.clear()
    # first_edge = pairs[0]
    # available_slots = topology.graph[first_edge[0]][first_edge[1]]['available_slots']
    blocked = _cal_possible_connections(list_of_avail_slots, slots, pairs)
    print("list_of_avail_slots {}".format(list_of_avail_slots))
    list_of_avail_slots.clear()
    return blocked, bvt, mod_type


# for i in traffic:
#     if traffic[i] > 0:
#         blocked_connections.append(i)
#
# print(blocked_connections)
# for i in blocked_connections:
#     print(i)

def main():
    accepted_connections = {}
    blocked_connections = []
    transponders = 0

    blocked = True
    ## For visualizing the graph
    # pos = nx.get_node_attributes(topology.graph, 'pos')
    # pos= nx.spring_layout(topology.graph)
    # #pos=nx.random_layout(topology.graph, seed=14)
    # #pos = nx.nx_agraph.graphviz_layout(topology.graph)
    # labels = nx.get_edge_attributes(topology.graph, 'linkDist')
    # nx.draw(topology.graph, pos, with_labels=True,node_color='skyblue', node_size=220, font_size=8, font_weight="bold")
    # nx.draw_networkx_edge_labels(topology.graph,pos, edge_labels=labels)
    # plt.savefig("TopologyVisual.png")
    # plt.clf()
    for i in symmetric_traffic:

        if symmetric_traffic[i] > 0:
            blocked = True
            for j in range(0, 2):
                # choose shortest path first

                link = links[i[0], i[1], j]

                isBlocked, bvt, mod_type = _cal_spectral_assignment(link, symmetric_traffic[i])
                if not isBlocked:
                    # print('Accepted Links are {}'.format(link))
                    blocked = False
                    accepted_connections[i] = [link, mod_type, bvt, symmetric_traffic[i]]
                    transponders = transponders + bvt
                    break


            if blocked:
                blocked_connections.append(i)
        else:
            print("negative traffic = {}".format(symmetric_traffic[i]))

    # print("traffic demand size= {}".format(len(symmetric_traffic)))
    #
    with open("BlockedConnections.txt", "a") as myfile:
        myfile.write(str(blocked_connections))
        myfile.write("\n")
    myfile.close()
    with open("Accepted connections.txt", "a") as myfile:
        myfile.write(str(accepted_connections))
        myfile.write("\n")

    myfile.close()
    print("All Blocked Connections are: {}".format(blocked_connections))
    print("All Accepted connections are: \n")

    print("All Accepted connections are {}".format(len(accepted_connections)))
    # print("Total number of Roadms {}".format(regen))
    #
    #
    # print("Total number of transponders {}".format(transponders))

    conn=[]
    for i in accepted_connections:
         conn.append(i)
    print(conn)
    way=[]
    for l in links:

        if l[2] == 0:
            way.append((l[0],l[1]))
    x=set(conn)
    y=set(way)
    z= y.difference(x)
    # print("Difference of first and second String: " + str(z))

    # pos = nx.get_node_attributes(topology.graph, 'pos')
    # pos= nx.spring_layout(topology.graph)
    # #pos=nx.random_layout(topology.graph, seed=13)
    # labels = nx.get_edge_attributes(topology.graph, 'used_capacity')
    # nx.draw(topology.graph, pos, with_labels=True,node_color='skyblue', node_size=220, font_size=8, font_weight="bold")
    # nx.draw_networkx_edge_labels(topology.graph,pos, edge_labels=labels)
    # plt.savefig("TopologyVisual_Connected.png")
    # plt.clf()
    # #
    # topology.graph['Berlin']['Hannover']['available_slots'] = []
    # topology.graph['Hannover']['Bremen']['available_slots'] = []
    # topology.graph['Berlin']['Hamburg']['available_slots'] = [1, 2, 6, 7, 9]
    # topology.graph['Hamburg']['Bremen']['available_slots'] = [0, 3, 4, 5, 6, 7, 8, 9]
    # #
    # for j in range(0, 2):
    #     # choose shortest path first
    #     link = links['Berlin', 'Bremen', j]
    #     print(link[1])
    #     isBlocked, regen = _cal_spectral_assignment(link, 41)
    #     if not isBlocked:
    #         print("Selected Path {}".format(link))
    #         break


if __name__ == "__main__":
    main()
