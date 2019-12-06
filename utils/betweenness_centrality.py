import networkx as nx

def single_betweenness_centrality(G, source, target, weight=None):
    """single point to point betweenness centrality.
        Source and target are single point

    """
    return nx.algorithms.centrality.betweenness_centrality_subset(G,  [source], [target],weight='latency')



# import networkx as nx
# sum_paths  = 0
# node_and_times = dict.fromkeys(substrate_network.nodes(), 0)
# paths = nx.all_shortest_paths(substrate_network, src, dst)  # generator of lists
# for path in paths:
#     sum_paths += 1
#     # stats nodes passing through shortest path
#     for node in path[1:-1]:  # intermediate nodes
#         node_and_times[node] += 1
# print node_and_times
# bc = {k: v * 1.0 / sum_paths for k, v in node_and_times.items()}