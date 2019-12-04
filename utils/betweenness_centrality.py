import networkx as nx

def single_betweenness_centrality(G, source, target, weight=None):
    """single point to point betweenness centrality.
        Source and target are single point

    """
    return nx.algorithms.centrality.betweenness_centrality_subset(G,  [source], [target], normalized=True,weight='latency')