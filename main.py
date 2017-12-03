from core.net import Net
from core.sfc import SFC
from core.vnf import VNF

# create a new substrate network
substrate_network = Net()
substrate_network.init_bandwidth_capacity(1, 6, 100)
substrate_network.init_bandwidth_capacity(1, 2, 100)
substrate_network.init_bandwidth_capacity(2, 3, 100)
substrate_network.init_bandwidth_capacity(3, 4, 100)
substrate_network.init_bandwidth_capacity(4, 5, 100)
substrate_network.init_bandwidth_capacity(5, 6, 100)
substrate_network.init_bandwidth_capacity(2, 6, 100)
substrate_network.init_bandwidth_capacity(2, 5, 100)
substrate_network.init_bandwidth_capacity(3, 5, 100)

substrate_network.init_link_latency(1, 6, 2)
substrate_network.init_link_latency(1, 2, 2)
substrate_network.init_link_latency(2, 3, 2)
substrate_network.init_link_latency(3, 4, 2)
substrate_network.init_link_latency(4, 5, 2)
substrate_network.init_link_latency(5, 6, 2)
substrate_network.init_link_latency(2, 6, 2)
substrate_network.init_link_latency(2, 5, 2)
substrate_network.init_link_latency(3, 5, 2)

substrate_network.init_node_cpu_capacity(1, 100)
substrate_network.init_node_cpu_capacity(2, 100)
substrate_network.init_node_cpu_capacity(3, 100)
substrate_network.init_node_cpu_capacity(4, 100)
substrate_network.init_node_cpu_capacity(5, 100)
substrate_network.init_node_cpu_capacity(6, 100)


src_vnf = VNF('src')
src_vnf.set_cpu_request(0)
src_vnf.set_outcome_interface_banwdith(20)
dst_vnf = VNF('dst')
dst_vnf.set_cpu_request(0)
sfc = SFC(src_vnf, dst_vnf)
vnf1 = VNF(1)
vnf1.set_cpu_request(10)
vnf1.set_outcome_interface_banwdith(10)
vnf2 = VNF(2)
vnf2.set_cpu_request(20)
vnf2.set_outcome_interface_banwdith(20)
vnf3 = VNF(3)
vnf3.set_cpu_request(30)
vnf3.set_outcome_interface_banwdith(30)
sfc.add_vnf(vnf1)
sfc.add_vnf(vnf2)
sfc.add_vnf(vnf3)
sfc.connect_two_vnfs(src_vnf, vnf1)
sfc.connect_two_vnfs(vnf1, vnf2)
sfc.connect_two_vnfs(vnf2, vnf3)
sfc.connect_two_vnfs(vnf3, dst_vnf)
sfc.set_latency_request(10)
sfc.set_src_substrate_node(1)
sfc.set_dst_substrate_node(4)

from algorithms.alg1 import ALG1
alg1 = ALG1()
alg1.install_substrate_network(substrate_network)
alg1.install_SFC(sfc)
alg1.start_algorithm()
new_sfc = alg1.get_new_sfc()
new_substrate_network = alg1.get_new_substrate_network()
print ""
