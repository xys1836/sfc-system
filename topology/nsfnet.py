import networkx as nx
import matplotlib.pyplot as plt
from core.net import Net
import random
simple_six_node_topology = None


bandwidth_capacity = 1000
cpu_capacity = 100

def generate_substrate_network():
    substrate_network = Net()
    substrate_network.init_bandwidth_capacity(0, 1, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(0, 2, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(0, 3, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(1, 2, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(1, 7, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(2, 5, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(3, 4, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(3, 10, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(4, 5, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(4, 6, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(5, 9, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(5, 12, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(6, 7, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(7, 8, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(8, 9, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(8, 11, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(8, 13, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(10, 11, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(10, 13, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(11, 12, bandwidth_capacity)
    substrate_network.init_bandwidth_capacity(12, 13, bandwidth_capacity)

    substrate_network.init_link_latency(0, 1, 1)
    substrate_network.init_link_latency(0, 2, 2)
    substrate_network.init_link_latency(0, 3, 3)
    substrate_network.init_link_latency(1, 2, 3)
    substrate_network.init_link_latency(1, 7, 7)
    substrate_network.init_link_latency(2, 5, 4)
    substrate_network.init_link_latency(3, 4, 3)
    substrate_network.init_link_latency(3, 10, 8)
    substrate_network.init_link_latency(4, 5, 2)
    substrate_network.init_link_latency(4, 6, 2)
    substrate_network.init_link_latency(5, 9, 6)
    substrate_network.init_link_latency(5, 12, 8)
    substrate_network.init_link_latency(6, 7, 2)
    substrate_network.init_link_latency(7, 8, 2)
    substrate_network.init_link_latency(8, 9, 6)
    substrate_network.init_link_latency(8, 11, 5)
    substrate_network.init_link_latency(8, 13, 5)
    substrate_network.init_link_latency(10, 11, 4)
    substrate_network.init_link_latency(10, 13, 6)
    substrate_network.init_link_latency(11, 12, 6)
    substrate_network.init_link_latency(12, 13, 3)

    substrate_network.init_node_cpu_capacity(0, cpu_capacity)
    substrate_network.init_node_cpu_capacity(1, cpu_capacity)
    substrate_network.init_node_cpu_capacity(2, cpu_capacity)
    substrate_network.init_node_cpu_capacity(3, cpu_capacity)
    substrate_network.init_node_cpu_capacity(4, cpu_capacity)
    substrate_network.init_node_cpu_capacity(5, cpu_capacity)
    substrate_network.init_node_cpu_capacity(6, cpu_capacity)
    substrate_network.init_node_cpu_capacity(7, cpu_capacity)
    substrate_network.init_node_cpu_capacity(8, cpu_capacity)
    substrate_network.init_node_cpu_capacity(9, cpu_capacity)
    substrate_network.init_node_cpu_capacity(10, cpu_capacity)
    substrate_network.init_node_cpu_capacity(11, cpu_capacity)
    substrate_network.init_node_cpu_capacity(12, cpu_capacity)
    substrate_network.init_node_cpu_capacity(13, cpu_capacity)

    substrate_network.pre_get_single_source_minimum_latency_path()
    substrate_network.update()

    return substrate_network

NSFNET = generate_substrate_network()

if __name__ == '__main__':
    substrate_network = generate_substrate_network()
    nx.draw(substrate_network)  # networkx draw()
    plt.draw()  # pyplot draw()
    plt.show()