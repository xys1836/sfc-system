from core.net import Net
from core.sfc import SFC
from core.vnf import VNF
import random

# create a new substrate network
substrate_network = Net()

bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(0, 1, bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(1, 6,  bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(1, 2, bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(2, 3,  bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(3, 4, bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(4, 5,  bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(5, 6,  bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(2, 6,  bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(2, 5, bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(3, 5, bw)
bw = random.randint(50, 100)
# bw = 100
substrate_network.init_bandwidth_capacity(4, 7, bw)

substrate_network.init_link_latency(0, 1, 2)
substrate_network.init_link_latency(1, 6, 2)
substrate_network.init_link_latency(1, 2, 2)
substrate_network.init_link_latency(2, 3, 2)
substrate_network.init_link_latency(3, 4, 2)
substrate_network.init_link_latency(4, 5, 2)
substrate_network.init_link_latency(5, 6, 2)
substrate_network.init_link_latency(2, 6, 2)
substrate_network.init_link_latency(2, 5, 2)
substrate_network.init_link_latency(3, 5, 2)
substrate_network.init_link_latency(4, 7, 2)

substrate_network.init_node_cpu_capacity(0, 100)
substrate_network.init_node_cpu_capacity(1, 100)
substrate_network.init_node_cpu_capacity(2, 100)
substrate_network.init_node_cpu_capacity(3, 100)
substrate_network.init_node_cpu_capacity(4, 1)
substrate_network.init_node_cpu_capacity(5, 100)
substrate_network.init_node_cpu_capacity(6, 100)
substrate_network.init_node_cpu_capacity(7, 100)
