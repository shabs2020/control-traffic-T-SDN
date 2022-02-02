

import networkx as nx
import json
import matplotlib.pyplot as plt
import math


## Open the files containing edges and nodes
from networkx.algorithms.flow import shortest_augmenting_path

with open("/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Nodes_Germany_17.json") as node_file:
    nodes=json.load(node_file)
with open("/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Links_Germany_17.json") as edge_file:
    edges=json.load(edge_file)

degree=0 # total degree of all the nodes in a given graph. set to 0 before the graph initialization
traffic ={} # traffic matrix from each source to non-disjoint targets.
assigned_path =[]
blocked_connections = []
## create the networkX graph
G = nx.Graph()
for e in nodes:
     G.add_node(nodes[e][0],lon=nodes[e][1], lat=nodes[e][2], num_of_IXPs= nodes[e][3],num_of_DCs=nodes[e][4])
for e in edges:
    # print(edges[e])
    G.add_edge(edges[e]['startNode'],edges[e]['endNode'], linkDist=edges[e]['linkDist'], noChannels=edges[e]['noChannels'], noSpans=edges[e]['noSpans'], spanList=edges[e]['spanList'], capacity=4400)


## For visualizing the graph
nx.draw(G,with_labels = True)
plt.savefig("TopologyVisual.png")
plt.clf()

# calculate avg. node degree
for node in G.nodes():
    degree=degree+G.degree(node)
avg_nodal_degree= degree/G.number_of_nodes()
print(avg_nodal_degree)



def _cal_traffic_matrix(i,j,k):
    combined_node_degree =G.degree(i) + G.degree(j)
    del_i = G.nodes[i]["num_of_IXPs"] - G.nodes[i]["num_of_DCs"]
    del_j = G.nodes[j]["num_of_IXPs"] - G.nodes[j]["num_of_DCs"]
    if(combined_node_degree>2*avg_nodal_degree):
        bin_coff = (math.factorial(combined_node_degree))/(math.factorial(2)*math.factorial(combined_node_degree-2))
        # traffic[(i,j)] =  2*bin_coff*del_i*del_j
        traffic[k] = [i,j, 2 * bin_coff * del_i * del_j]
    else:
        # traffic[(i,j)] = combined_node_degree*del_i*del_j
        traffic[k] = [i,j, combined_node_degree * del_i * del_j]
    return traffic[k]


counter = 0 # Used as the key for the traffic matrix dictionary. will increment by 1 for each traffic element
for i in G.nodes:
    for j in G.nodes:
        if(i==j):
            traffic[counter]=[i,j,0]
            #traffic[(i,j)] = 0

        else:
            _cal_traffic_matrix(i,j, counter)
        counter =  counter + 1
print(counter)
# Print traffic into a file
f = open("traffic_demand.json", "a")
f.write(json.dumps(traffic))
f.close()

## Route Assignment

def _cal_route_assignment(i, j, amt):
    no_of_slots = math.ceil(amt / 12.5)
    paths = nx.shortest_simple_paths(G, source=i, target=j, weight='linkDist')
    req_capacity = no_of_slots * 12.5

    for a in range(0, 2):
        select_path = next(paths)
        find_path = _find_edges_in_path(select_path, req_capacity)
        if (find_path != False):
            assigned_path.append(select_path)
            print("assigned_path: {} ".format(assigned_path))
            break
    if select_path not in assigned_path:
        blocked_connections.append([i,j])
        print("blocked_connections : {}" .format(blocked_connections))


def _find_edges_in_path(path, capacity):
    pairs = [path[i: i + 2] for i in range(len(path) - 1)]
    count=0
    allocated_slots=[]

    for pair in pairs:

        # check for each link or edge given path

        if(G[pair[0]][pair[1]]['capacity'] < capacity):
            check_path = False
            break
        else:
            G[pair[0]][pair[1]]['capacity'] = G[pair[0]][pair[1]]['capacity'] - capacity
            check_path = True
        print("capcity for {} {}".format(pair[0], pair[1]))
        print(G[pair[0]][pair[1]]['capacity'])
    return check_path

G['Berlin']['Leipzig']['capacity'] = G['Berlin']['Leipzig']['capacity'] -4400
_cal_route_assignment('Berlin','Mannheim', 340)
# from networkx.algorithms.connectivity import build_auxiliary_node_connectivity
#
# H = build_auxiliary_node_connectivity(G)
# from networkx.algorithms.flow import build_residual_network
# R = build_residual_network(H, "linkDist")
x = nx.edge_disjoint_paths(G,'Berlin','Leipzig', cutoff=2)
disjoint_paths=[]
shortest_path=[]
for i in traffic.items():
    if i[1][2] != 0:
        x = nx.node_disjoint_paths(G, i[1][0], i[1][1], cutoff=2)
        y = nx.shortest_simple_paths(G, i[1][0], i[1][1], weight='linkDist')

        for path in x:
            disjoint_paths.append(path)
        for i in range(0,2):
            shortest_path.append(next(y))

print(disjoint_paths)
print(len(disjoint_paths))
print(shortest_path)
print(len(shortest_path))

