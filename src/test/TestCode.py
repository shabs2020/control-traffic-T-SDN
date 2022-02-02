import math
import json
# m = [1,2,4,6,6,7,8,9,11]
# c =[]
# c=m.copy()
# print(c)
#
# list_one=[1,2,3,4]
# list_two=[1,2,3,4,5,6]
# if all(a in list_two for a in list_one):
#     print("yes")
# from Topology import _Topology
# import json
# import math
#
# import Modulation
# import matplotlib.pyplot as plt
# #
# import networkx as nx
#
# with open(
#         "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Nodes_Germany_17.json") as node_file:
#     nodes = json.load(node_file)
# with open(
#         "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Links_Germany_17.json") as edge_file:
#     edges = json.load(edge_file)
#
# with open("/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Demands_Germany_17_init_traff.json") as demand_file:
#     demands = json.load(demand_file)
# demand={}
# print("demand {}".format(demands))
# for i in demands:
#     demand[(demands[i][0],demands[i][1])] = demands[i][2]
#
# print((demand))
# #
# topology = _Topology(nodes, edges)
#
# traffic = {}
# for i in topology.graph.nodes:
#     for j in topology.graph.nodes:
#         if i=='Berlin' and j =='Leipzig':
#             print(topology.graph.degree('Berlin'))
#             print(topology.graph.degree('Leipzig'))
#             combined_node_degree = topology.graph.degree(i) + topology.graph.degree(j)
#             print(topology.graph.nodes[i]["num_of_DCs"])
#             print(topology.graph.nodes[i]["num_of_IXPs"])
#             del_i = topology.graph.nodes[i]["num_of_DCs"]-topology.graph.nodes[i]["num_of_IXPs"]
#             del_j = topology.graph.nodes[j]["num_of_DCs"]-topology.graph.nodes[j]["num_of_IXPs"]
#             print(del_j)
#             print(del_i)
#             print(2*topology.avg_nodal_degree)
#             if (combined_node_degree > 2 * topology.avg_nodal_degree):
#                 print(math.factorial(combined_node_degree))
#                 print(math.factorial(2))
#                 print(math.factorial(combined_node_degree - 2))
#                 bin_coff = (math.factorial(combined_node_degree)) / (
#                         math.factorial(2) * math.factorial(combined_node_degree - 2))
#                 # traffic[(i,j)] =  2*bin_coff*del_i*del_j
#                 traffic[i, j] = 2 * bin_coff * del_i * del_j
#             else:
#                 # traffic[(i,j)] = combined_node_degree*del_i*del_j
#                 traffic[i, j] = combined_node_degree * del_i * del_j
#
# print(traffic)


# Test the continuous and contiguous slots
# main_list=[]
# list1=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,18,19,20]
# list2=[0, 1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 16,17,18]
# list3=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17,18,19,20]
# main_list.append(list1)
# main_list.append(list2)
# main_list.append(list3)
# print(main_list)
# main_list.clear()
# print(main_list)
#
# while True:
#
#     inp = input("Enter the number of slots")
#     common_items = set.intersection(*map(set, main_list))
#     common_elements = list(common_items)
#     print('common_elements {}'.format(common_elements))
#     ranges = sum((list(t) for t in zip(common_elements, common_elements[1:]) if t[0] + 1 != t[1]), [])
#     iranges = iter(common_elements[0:1] + ranges + common_elements[-1:])
#     continuity = False
#     if iranges:
#         for n in iranges:
#             initial_slot = n
#             end_slot = next(iranges)
#             required_slots_last_index = (initial_slot + int(inp)) - 1
#
#             if (required_slots_last_index) > end_slot:
#                 print("proper slots not found")
#                 continuity=False
#                 continue
#             else:
#                 candidate_slots = [x for x in range(initial_slot, required_slots_last_index + 1)]
#                 print("proper slots  found {}".format(candidate_slots))
#                 continuity=True
#                 break
#
#     if continuity:
#         for l in range(0, len(main_list)):
#             main_list[l]=[item for item in main_list[l] if item not in candidate_slots]
#
#
#     print(main_list)

# End of continuity/contiguity test

traffic_demand = {}
with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Demands_Germany_17_init_traff.json") as demand_file:
    demands = json.load(demand_file)
for i in demands:
    traffic_demand[(demands[i][0], demands[i][1])] = demands[i][2]
print(len(traffic_demand))

