from core.vnf import VNF
from core.vnf import VNFType

class VNFDST(VNF):
    """
    This vnf is output the same volume of input
    """
    def __init__(self):
        VNF.__init__(self, id = 'dst')
        self.type = VNFType.DST
        self.set_cpu_request(0)

    def vnf_bw(self, i):
        return 0

