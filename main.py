import networkx as nx
import osmnx as ox

G = ox.graph_from_point((38.06832 , 46.32453), dist=750, network_type="drive")
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)
D = ox.utils_graph.get_digraph(G, weight="length")

intact_shortest_paths = list(nx.all_pairs_dijkstra(D, weight="length"))

length_diffs = []
node_diffs = []
for edge in G.edges:
    if G.degree(edge[0]) <= 1 or G.degree(edge[1]) <= 1: continue
    H = G.copy()
    H.remove_edge(*edge)
    shortest_paths = list(nx.all_pairs_dijkstra(H, weight="length"))

    length_diff = 0
    node_diff = 0
    for shortest_path in shortest_paths:
        intact_shortest_path = None
        for x in intact_shortest_paths:
            if x[0] == shortest_path[0]:
                intact_shortest_path = x
                break

        for node in shortest_path[1][0]:
            length_diff += shortest_path[1][0][node] - intact_shortest_path[1][0][node]

        node_diff += len(intact_shortest_path[1][0]) - len(shortest_path[1][0])

    length_diffs.append(round(length_diff))
    node_diffs.append(node_diff)