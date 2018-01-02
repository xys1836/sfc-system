import networkx as nx
# import matplotlib.pyplot as plt
from core.net import Net
from core.sfc import SFC
from core.vnf import VNF
import random

# create a new substrate network
substrate_network = Net()

number_of_nodes = 10
probability = 0.5
topology = nx.erdos_renyi_graph(number_of_nodes, probability, seed=None, directed=False)
network_create_counter = 0
while not nx.is_connected(topology):
    if network_create_counter >= 10000:
        break
    network_create_counter += 1
    topology = nx.erdos_renyi_graph(number_of_nodes, probability, seed=None, directed=False)


for edge in topology.edges():
    bw = random.randint(100, 200)
    substrate_network.init_bandwidth_capacity(edge[0], edge[1], bw)
    lt = random.uniform(0.5, 1.5)
    substrate_network.init_link_latency(edge[0], edge[1], lt)

for node in topology.nodes():
    cpu_capacity = random.randint(100, 200)
    substrate_network.init_node_cpu_capacity(node, cpu_capacity)

substrate_network.update()
substrate_network.print_out_nodes_information()
substrate_network.print_out_edges_information()



