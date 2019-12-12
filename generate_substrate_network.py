import networkx as nx
# import matplotlib.pyplot as plt
from core.net import Net
import random
import matplotlib.pyplot as plt

def generate_random_network(number_of_node, probability):
    # create a new substrate network
    substrate_random_network = Net()

    number_of_nodes = number_of_node
    probability = probability
    topology = nx.erdos_renyi_graph(number_of_nodes, probability, seed=None, directed=False)
    network_create_counter = 0
    while not nx.is_connected(topology):
        if network_create_counter >= 10000:
            break
        network_create_counter += 1
        topology = nx.erdos_renyi_graph(number_of_nodes, probability, seed=None, directed=False)

    for edge in topology.edges():
        bw = random.randint(50, 100)
        substrate_random_network.init_bandwidth_capacity(edge[0], edge[1], bw)
        lt = random.uniform(1, 5)
        substrate_random_network.init_link_latency(edge[0], edge[1], lt)

    for node in topology.nodes():
        cpu_capacity = random.randint(50, 100)
        substrate_random_network.init_node_cpu_capacity(node, cpu_capacity)
    substrate_random_network.pre_get_single_source_minimum_latency_path()
    substrate_random_network.update()
    return substrate_random_network

if __name__ == '__main__':
    substrate_random_network = generate_random_network(100, 0.2)
    # bc = nx.algorithms.centrality.betweenness_centrality(substrate_random_network, weight='latency')

    nx.draw(substrate_random_network)
    plt.show()
    # print bc
