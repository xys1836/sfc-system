from core.vnf import VNF
from core.vnf import VNFType

class VNFType1(VNF):
    """
    This vnf is output the same volumn of input
    """
    def __init__(self, id):
        VNF.__init__(self, id)
        self.type = VNFType.TYPE1

    def vnf_bw(self, i):
        return i

