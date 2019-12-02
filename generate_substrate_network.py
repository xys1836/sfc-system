import networkx as nx
# import matplotlib.pyplot as plt
from core.net import Net
from core.sfc import SFC
from core.vnf import VNF
import random

# create a new substrate network
substrate_random_network = Net()

number_of_nodes = 100
probability = 0.2
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
substrate_random_network.print_out_nodes_information()
substrate_random_network.print_out_edges_information()



