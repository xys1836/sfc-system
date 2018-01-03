from core.vnf import VNFType, VNF
from vnfs.vnf_type_1 import VNFType1

"""
{type: "TYPE1", "name": "vnf1", "CPU": 100},
"""
class VNFGenerator():
    @classmethod
    def generate(cls, vnf_dict):
        vnf_type = vnf_dict["type"]
        vnf_name = vnf_dict["name"]
        vnf_cpu_request = vnf_dict["CPU"]
        if vnf_type == VNFType.TYPE1:
            vnf = VNFType1(vnf_name)
            vnf.set_cpu_request(vnf_cpu_request)
            return vnf
        elif vnf_type == VNFType.TYPE2:
            print "TYPE 2 is not defined. exit"
            exit(1)
        else:
            print "TYPE is existed, exit"
            exit(1)


