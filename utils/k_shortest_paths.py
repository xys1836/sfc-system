import networkx as nx
from itertools import islice

def k_shortest_paths(G, source, target, k, weight=None):
    """Calculate k shortest paths
    :param G: networkx topology
           source: source node
           target: target node
           k: the number of shortest paths
           weight: weight for calculation of shortest path
    :return: a list of k shortest paths
    """
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))