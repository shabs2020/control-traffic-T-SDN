import fnss
import networkx as nx
import json
import matplotlib.pyplot as plt
import math
import numpy as np
import scipy as sp

## Open the files containing edges and nodes
with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Nodes_Germany_17.json") as node_file:
    nodes = json.load(node_file)
with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Links_Germany_17.json") as edge_file:
    edges = json.load(edge_file)

## Read initial traffic
with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Demands_Germany_17_init_traff.json") as traffic_file:
    weights = json.load(traffic_file)

## create the networkX graph
G = nx.Graph()
for e in nodes:
    #
    G.add_node(nodes[e][0], lon=nodes[e][1], lat=nodes[e][2], num_of_IXPs=nodes[e][3], num_of_DCs=nodes[e][4])
#
# print(G.nodes())
# print(nx.get_node_attributes(G,'lat'))

for e in edges:
    # print(edges[e])
    G.add_edge(edges[e]['startNode'], edges[e]['endNode'], linkDist=edges[e]['linkDist'],
               noChannels=edges[e]['noChannels'], noSpans=edges[e]['noSpans'], spanList=edges[e]['spanList'],
               capacity=4400, available_slots=list(range(0,351)), used_slots=[])
# print("edges are {}" .format(G.edges()))
# print(nx.get_edge_attributes(G,'spanList'))


## For visualizing the graph
nx.draw(G, with_labels=True)
plt.savefig("TopologyVisual.png")
plt.clf()

degree = 0
for node in G.nodes():
    degree = degree + G.degree(node)
# print(degree)
# print(G.number_of_nodes())
avg_nodal_degree = degree / G.number_of_nodes()
# print(avg_nodal_degree)
for edge in G.edges():
    combined_node_degree = 0
    # print(edge[0])
    combined_node_degree = G.degree(edge[0]) + G.degree(edge[1])
#  print(combined_node_degree)
print(G.edges)
A = nx.to_numpy_matrix(G, nodelist=None)
d = nx.adjacency_matrix(G, weight=2)
# print(A)
# print(G.get_edge_data('Berlin', 'Hamburg'))

traffic = {}
blocked_connections=[]
assigned_path=[]


def _cal_traffic_matrix(i, j, k):
    combined_node_degree = G.degree(i) + G.degree(j)
    del_i = G.nodes[i]["num_of_IXPs"] - G.nodes[i]["num_of_DCs"]
    del_j = G.nodes[j]["num_of_IXPs"] - G.nodes[j]["num_of_DCs"]
    if (combined_node_degree > 2 * avg_nodal_degree):
        bin_coff = (math.factorial(combined_node_degree)) / (
                    math.factorial(2) * math.factorial(combined_node_degree - 2))
        # traffic[(i,j)] =  2*bin_coff*del_i*del_j
        traffic[k] = [i, j, 2 * bin_coff * del_i * del_j]
    else:
        # traffic[(i,j)] = combined_node_degree*del_i*del_j
        traffic[k] = [i, j, combined_node_degree * del_i * del_j]
    return traffic[k]


# traffic_test= _cal_traffic_matrix('Berlin','Mannheim')

counter = 0
for i in G.nodes:
    for j in G.nodes:
        if (i == j):
            traffic[counter] = [i, j, 0]
            # traffic[(i,j)] = 0

        else:
            _cal_traffic_matrix(i, j, counter)
        counter = counter + 1
print(counter)

f = open("traffic_demand.json", "a")
f.write(json.dumps(traffic))
f.close()


def _cal_shortest_path(i, j):
    sp = nx.shortest_path(G, source=i, target=j, weight='linkDist')
    return sp


sp = nx.shortest_path(G, source='Berlin', target='Mannheim', weight='linkDist')

ap = nx.shortest_simple_paths(G, source='Berlin', target='Mannheim', weight='linkDist')

# for a in range(3):
#     print(next(ap))
#
# print(next(ap))
# print(next(ap))
# print(next(ap))
# print(A)
# print(d.todense())

G['Berlin']['Leipzig']['capacity'] = G['Berlin']['Leipzig']['capacity'] -4400
#G['Berlin']['Hannover']['capacity'] = G['Berlin']['Hannover']['capacity'] -4400

#G['Leipzig']['Frankfurt']['capacity'] = G['Leipzig']['Frankfurt']['capacity'] -4200


def _cal_route_assignment(i, j, amt):
    no_of_slots = round(amt / 12.5)
    paths = nx.shortest_simple_paths(G, source=i, target=j, weight='linkDist')
    req_capacity = no_of_slots * 12.5
    check_assigned_paths = len(assigned_path)
    blocked=0
    for a in range(0, 2):
        select_path = next(paths)
        find_path = _find_edges_in_path(select_path, req_capacity,no_of_slots)
        if (find_path != False):
            assigned_path.append(select_path)
            new_check_assigned_paths = len(assigned_path)
            print("assigned_path: {} ".format(assigned_path))
            break
    if select_path not in assigned_path:
        blocked_connections.append([i,j])
        print("blocked_connections : {}" .format(blocked_connections))


def _find_edges_in_path(path, capacity,no_of_slots):
    assigned_path = path
    pairs = [path[i: i + 2] for i in range(len(path) - 1)]
    count=0
    allocated_slots=[]


    for pair in pairs:
        print("capcity for {} {}".format(pair[0], pair[1]) )
        # check for each link or edge given path


        print(G[pair[0]][pair[1]]['capacity'])
        if(G[pair[0]][pair[1]]['capacity'] < capacity):
            check_path = False
            return check_path
            break
        else:
            G[pair[0]][pair[1]]['capacity'] = G[pair[0]][pair[1]]['capacity'] - capacity
            if count==0:
                candidate_slots = G[pair[0]][pair[1]]['available_slots'].copy()
                allocated_slots,check_path=(_spec_assign_initial(G[pair[0]][pair[1]],candidate_slots,no_of_slots))
                count +=1

            else:
                check_path=_spec_assign(G[pair[0]][pair[1]], allocated_slots)

    return check_path


print(G['Berlin']['Hannover']['capacity'])
print(G['Hannover']['Frankfurt']['capacity'])
# for a in range(0, 2):
#     select_path= next(ap)
#     print(select_path)
#     check_path = True
#     find_path = _find_edges_in_path(select_path, 340)
#     if (find_path != False):
#         assigned_path.append(select_path)
#         break
#     print("path {}" .format(find_path) )

def _allocate_slots(edge,element)  :
    edge['available_slots'].remove(element)
    edge['used_slots'].append(element)

def _retain_slots(edge,element)  :
    edge['available_slots'].append(element)
    edge['used_slots'].remove(element)
def _spec_assign_initial(edge,slots,no_of_slots):

    avail_slots=slots
    print(avail_slots)

    # Find the groups of continuous slots
    ranges = sum((list(t) for t in zip(avail_slots, avail_slots[1:]) if t[0] + 1 != t[1]), [])
    iranges = iter(avail_slots[0:1] + ranges + avail_slots[-1:])
    if iranges:
        for n in iranges:
            begin_slot = n
            end_slot  = next(iranges)
            req_slots = begin_slot + no_of_slots

            if no_of_slots <= end_slot:
                if all(a in edge['available_slots'] for a in req_slots):



                    _allocate_slots(edge,x)
                print("Available Slots {}".format(edge['available_slots']))
                print("Usedlots {}".format(edge['used_slots']))
                return edge['used_slots'], True
            else:
                return None, False

    else:
        print("no Contiguos slots avaialable")
        return None, False

def _spec_assign(edge,slots):
    if all(a in edge['available_slots'] for a in slots):
        for x in slots:
            #print(x)
            _allocate_slots(edge,x)
        return True
    else:
        return False

#_cal_route_assignment('Berlin','Mannheim', 40)
#x=_spec_assign(G['Berlin']['Leipzig'],[0,1,2])

#print(x)



# print(G['Berlin']['Hannover']['available_slots'])
# slots = 3
# #
#
# nums = [2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 20]
# # nums= G['Berlin']['Hannover']['available_slots']
# ranges = sum((list(t) for t in zip(nums, nums[1:]) if t[0] + 1 != t[1]), [])
# iranges = iter(nums[0:1] + ranges + nums[-1:])
#
# for n in iranges:
#
#     begin_slot = n
#     end_slot = next(iranges)
#     req_slots = n + slots
#
#     print(begin_slot)
#     print(end_slot)
#     print(req_slots)
#
#     if slots <= end_slot:
#
#         for x in range(begin_slot, req_slots + 1):
#             nums.remove(x)
#         break
#

#print( ', '.join([str(n) + '-' + str(next(iranges)) for n in iranges]))
#
# a=_spec_assign(G['Berlin']['Hannover'],G['Berlin']['Hannover']['available_slots'], 3)
# print(a)
# b=[]
# b.append(_spec_assign(G['Berlin']['Hannover'],G['Berlin']['Hannover']['available_slots'], 3))
# print(b)##
#x=_spec_assign_initial(G['Berlin']['Hannover'],G['Berlin']['Hannover']['available_slots'], 358)


def _find_available_slots(slots,no_of_slots):
    cand_slots=[]
    ranges = sum((list(t) for t in zip(slots, slots[1:]) if t[0] + 1 != t[1]), [])
    iranges = iter(slots[0:1] + ranges + slots[-1:])
    if iranges:
        for n in iranges:
            begin_slot = n
            end_slot=next(iranges)
            req_slots = (begin_slot + no_of_slots)-1
            if req_slots<=end_slot:
                cand_slots.append([begin_slot,req_slots])

        return cand_slots

#x = _find_available_slots(G['Berlin']['Hannover'],G['Berlin']['Hannover']['available_slots'], 30)
x=_find_available_slots([2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 20],4)

print('findandi slots {}'.format(x))

def _find_edges_in_path1(path):
    assigned_path = path
    pairs = [path[i: i + 2] for i in range(len(path) - 1)]

    count=0
    allocated_slots=[]

def _cal_route_assignment1(i, j, amt):
    no_of_slots = round(amt / 12.5)
    paths = nx.shortest_simple_paths(G, source=i, target=j, weight='linkDist')
    req_capacity = no_of_slots * 12.5
    check_assigned_paths = len(assigned_path)
    blocked = 0
    for a in range(0, 2):
        select_path = next(paths)
        find_path = _find_edges_in_path1(select_path, req_capacity, no_of_slots)
if all(a in G[pair[0]][pair[1]]['available_slots'] for a in slots):
    print('true')
for s in x:
    print(s[0])
