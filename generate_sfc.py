from core.sfc import SFC
from core.vnf import VNF
from vnfs.vnf_type_1 import VNFType1

# # src_vnf = VNF('src')
# src_vnf = VNFType1('src')
# src_vnf.set_cpu_request(0)
# # src_vnf.set_outcome_interface_bandwidth(20)
#
# dst_vnf = VNF('dst')
# dst_vnf.set_cpu_request(0)
# sfc = SFC(src_vnf, dst_vnf)
# vnf1 = VNF(1)
# vnf1.set_cpu_request(10)
# # vnf1.set_outcome_interface_bandwidth(10)
# vnf2 = VNF(2)
# vnf2.set_cpu_request(20)
# # vnf2.set_outcome_interface_bandwidth(20)
# vnf3 = VNF(3)
# vnf3.set_cpu_request(30)
# # vnf3.set_outcome_interface_bandwidth(30)
#
# sfc.id = 'sfc_1'
# sfc.add_vnf(vnf1)
# sfc.add_vnf(vnf2)
# sfc.add_vnf(vnf3)
# sfc.connect_two_vnfs(src_vnf, vnf1)
# sfc.connect_two_vnfs(vnf1, vnf2)
# sfc.connect_two_vnfs(vnf2, vnf3)
# sfc.connect_two_vnfs(vnf3, dst_vnf)
# sfc.set_input_throughput(10)
# sfc.set_latency_request(10)
#
# sfc.set_src_substrate_node(2)
# sfc.set_dst_substrate_node(8)
sfc_dict = {
    "name": "sfc_1",
    "type": "xx",
    "vnf_list": [
        {"type": 2, "name": "vnf1", "CPU": 10},
        {"type": 2, "name": "vnf2", "CPU": 20},
        {"type": 2, "name": "vnf3", "CPU": 30},
        {"type": 2, "name": "vnf4", "CPU": 40},

    ],
    "bandwidth": 20,
    "src_node": 1,
    "dst_node": 9,
    "latency": 10
}

from controllers.sfc_generator import SFCGenerator
sfc = SFCGenerator(sfc_dict).generate()
print ""