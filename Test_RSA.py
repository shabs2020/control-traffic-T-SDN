import fnss
import networkx as nx
import json
import matplotlib.pyplot as plt
import math

## Open the files containing edges and nodes
with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Nodes_Germany_17.json") as node_file:
    nodes = json.load(node_file)
with open(
        "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Links_Germany_17.json") as edge_file:
    edges = json.load(edge_file)

degree = 0  # total degree of all the nodes in a given graph. set to 0 before the graph initialization
traffic = {}  # traffic matrix from each source to non-disjoint targets.
assigned_path = []
blocked_connections = []
candidate_slots=[]
## create the networkX graph
G = nx.Graph()
for e in nodes:
    G.add_node(nodes[e][0], lon=nodes[e][1], lat=nodes[e][2], num_of_IXPs=nodes[e][3], num_of_DCs=nodes[e][4])
for e in edges:
    # print(edges[e])
    G.add_edge(edges[e]['startNode'], edges[e]['endNode'], linkDist=edges[e]['linkDist'],
               noChannels=edges[e]['noChannels'], noSpans=edges[e]['noSpans'], spanList=edges[e]['spanList'],
               capacity=125, available_slots=list(range(0, 10)), used_slots=[])

## For visualizing the graph
nx.draw(G, with_labels=True)
plt.savefig("TopologyVisual.png")
plt.clf()

# calculate avg. node degree
for node in G.nodes():
    degree = degree + G.degree(node)
avg_nodal_degree = degree / G.number_of_nodes()
print(avg_nodal_degree)


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


counter = 0  # Used as the key for the traffic matrix dictionary. will increment by 1 for each traffic element
for i in G.nodes:
    for j in G.nodes:
        if (i == j):
            traffic[counter] = [i, j, 0]
            # traffic[(i,j)] = 0

        else:
            _cal_traffic_matrix(i, j, counter)
        counter = counter + 1
print(counter)
# Print traffic into a file
f = open("traffic_demand.json", "a")
f.write(json.dumps(traffic))
f.close()


## Route Assignment

def _cal_route_assignment(i, j, amt):
    no_of_slots = math.ceil(amt / 6.25) + 6.25
    paths = nx.shortest_simple_paths(G, source=i, target=j, weight='linkDist')
    req_capacity = no_of_slots * 6.25
    check_continuos_slots = False

    for a in range(0, 2):
        select_path = next(paths)

        find_path = _find_edges_in_path(select_path, req_capacity, no_of_slots)
        if (find_path != False):
            assigned_path.append(select_path)

            break
    if select_path not in assigned_path:
        blocked_connections.append([i, j])


def _confirm_slots_through_path(path,slots):
    pairs = [path[i: i + 2] for i in range(len(path) - 1)]
    for pair in pairs:
        if all(a in G[pair[0]][pair[1]]['available_slots'] for a in slots):
            print('Continuous slots Available')
            return True
        else:
            return False
            break





def _find_edges_in_path(path, capacity, no_of_slots):
    print("selected Path: {}".format(path))
    pairs = [path[i: i + 2] for i in range(len(path) - 1)]
    count = 0
    allocated_slots = []
    first_edge=pairs[0]
    print(pairs[0])

    for pair in pairs:
        print("Available capacity for {} {}: {}".format(pair[0], pair[1], G[pair[0]][pair[1]]['capacity']))
        print("requested capacity {}".format(capacity))
        # check for each link or edge given path

        if (G[pair[0]][pair[1]]['capacity'] < capacity):
            check_path = False
            return check_path
            break
        else:
            # if pair==first_edge:
            #     candi_slots = _find_available_slots(G[pair[0]][pair[1]]['available_slots'])



            if count == 0:
                candidate_slots = G[pair[0]][pair[1]]['available_slots'].copy()
                allocated_slots, check_path = (_spec_assign_initial(G[pair[0]][pair[1]],  G[pair[0]][pair[1]]['available_slots'], no_of_slots))
                count += 1

            else:
                check_path = _spec_assign(G[pair[0]][pair[1]], allocated_slots) if allocated_slots is not None else False

    return check_path


def _allocate_slots(edge, element, no_of_slots):
    #print("Element and edge: {}, {}".format(element,edge))

    edge['available_slots'].remove(element)
    edge['used_slots'].append(element)


def _retain_slots(edge, element):

    edge['available_slots'].append(element)
    edge['used_slots'].remove(element)

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


def _spec_assign_initial(edge, slots, no_of_slots):
    avail_slots = slots
    print(avail_slots)

    # Find the groups of continuous slots
    ranges = sum((list(t) for t in zip(avail_slots, avail_slots[1:]) if t[0] + 1 != t[1]), [])
    iranges = iter(avail_slots[0:1] + ranges + avail_slots[-1:])
    if iranges:
        for n in iranges:
            begin_slot = n
            end_slot = next(iranges)
            req_slots = begin_slot + no_of_slots

            print('begin_slot : {}'.format(begin_slot))
            print('end_slot : {}'.format(end_slot))
            print('req_slots: {}'.format(req_slots))
            if req_slots <= end_slot:
                edge['capacity'] = edge['capacity'] - (no_of_slots * 12.5)
                for x in range(begin_slot, req_slots):
                    #print("available slots before alloc: {}".format(edge['available_slots']))
                    #print("required slots before alloc: {}".format(req_slots))

                    _allocate_slots(edge, x,no_of_slots)
                print("Available Slots after assignment{}".format(edge['available_slots']))
                print("Usedlots {}".format(edge['used_slots']))
                print("remaining capacity: {}".format(edge['capacity']))
                return edge['used_slots'], True
            else:
                return None, False

    else:
        print("no Contiguos slots avaialable")
        return None, False


def _spec_assign(edge, slots):
    print("avail slots before alloc: {}".format(edge['available_slots']))
    print("req slots before alloc: {}".format(slots))
    no_of_slots=len(slots)
    if all(a in edge['available_slots'] for a in slots):
        edge['capacity'] = edge['capacity'] - (no_of_slots * 12.5)
        for x in slots:
            # print(x)
            _allocate_slots(edge, x, (no_of_slots*12.5))
        return True
    else:
        return False


for t in traffic:

    if (traffic[t][2] != 0) & (traffic[t][0]=='Berlin'):
        print("Requested Connection: {}, {}".format(traffic[t][0],traffic[t][1]))
        _cal_route_assignment(traffic[t][0], traffic[t][1], traffic[t][2])
        print("assigned_path: {} ".format(assigned_path))
        print("blocked_connections : {}".format(blocked_connections))
# G['Stuttgart']['Ulm']['capacity'] = 0
# _cal_route_assignment('Berlin','Ulm', 100)
