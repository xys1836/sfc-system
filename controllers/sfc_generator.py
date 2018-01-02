from core.poisson_emitter import PoissonEmitter
from core.sfc import SFC
from core.vnf import VNF
from vnfs.vnf_type_src import VNFSRC
from vnfs.vnf_type_dst import VNFDST
from controllers.vnf_generator import VNFGenerator

"""
sfc_dict
{
    "name": "sfc1",
    "type": "xx",
    # "number_of_vnfs": 4,
    "vnf_list": [
        {type: "TYPE1", "name": "vnf1", "CPU": 100},
        {type: "TYPE1", "name": "vnf1", "CPU": 100},
        {type: "TYPE1", "name": "vnf1", "CPU": 100},
        {type: "TYPE1", "name": "vnf1", "CPU": 100},
        
    ],
    "bandwidth": 10,
    "src_node": 1,
    "dst_node": 9,
    "latency": 10
}
"""


class SFCGenerator():
    def __init__(self, sfc_dict):
        self.sfc_dict = sfc_dict
        self.sfc_name = sfc_dict["name"]
        self.vnf_id_list = sfc_dict["vnf_list"]
        self.bandwidth = sfc_dict["bandwidth"]
        self.src_substrate_node = sfc_dict["src_node"]
        self.dst_substrate_node = sfc_dict["dst_node"]
        self.latency = sfc_dict["latency"]


    def generate(self):
        vnfs_list = []
        src_vnf = VNFSRC()
        dst_vnf = VNFDST()
        sfc = SFC(src_vnf, dst_vnf)
        sfc.id = self.sfc_name
        sfc.set_src_substrate_node(self.src_substrate_node)
        sfc.set_dst_substrate_node(self.dst_substrate_node)

        vnfs_list.append(src_vnf)

        for vnf_dict in self.vnf_id_list:
            vnf = VNFGenerator.generate(vnf_dict)
            vnfs_list.append(vnf)
            sfc.add_vnf(vnf)

        vnfs_list.append(dst_vnf)
        for i in range(0, len(vnfs_list)-1):
            sfc.connect_two_vnfs(vnfs_list[i], vnfs_list[i+1])

        sfc.set_input_throughput(self.bandwidth)
        sfc.set_latency_request(self.latency)
        return sfc



