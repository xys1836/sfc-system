from core.vnf import VNF
class SFC():
    def __init__(self, vnf_src, vnf_dst):
        self.number_of_vnfs = 0 # This is not include src and dst
        self.vnfs = {}
        self.src = vnf_src
        self.dst = vnf_dst
        self.link_bandwidth_dict = {}
        self.latency_request = 0

    def add_vnf(self, vnf):
        self.vnfs[vnf.id] = vnf
        self.number_of_vnfs += 1

    def remove_vnf(self, vnf):
        exit(1)

    def set_src_substrate_node(self, substrate_node):
        """set substrate node for src

        This method assign a substrate node for hosting src in sfc.
        """
        # todo(xu): we need consider whether this method should in sfc class
        self.src.assign_substrate_node(substrate_node)

    def set_dst_substrate_node(self, substrate_node):
        """set substrate node for dst

                This method assign a substrate node for hosting src in sfc.
                """
        # todo(xu): we need consider whether this method should in sfc class
        self.dst.assign_substrate_node(substrate_node)

    def connect_two_vnfs(self, vnf1, vnf2):
        vnf1.set_next_vnf(vnf2)
        vnf2.set_previous_vnf(vnf1)
        link_bw = vnf1.get_outcome_interface_bandwidth()
        vnf2.set_income_interface_bandwidth(link_bw)
        self.link_bandwidth_dict[(vnf1.id, vnf2.id)] = link_bw

    def get_number_of_vnfs(self):
        return self.number_of_vnfs

    def get_vnf_cpu_request(self, vnf):
        return vnf.get_cpu_request()
    def get_link_bandwidth_request(self, vnf1_id, vnf2_id):
        return self.link_bandwidth_dict[(vnf1_id, vnf2_id)]
    def get_next_vnf(self, vnf):
        return vnf.get_next_vnf()
    def get_previous_vnf(self, vnf):
        return vnf.get_previous_vnf()
    def get_substrate_node(self, vnf):
        return vnf.get_substrate_node()
    def get_src_vnf(self):
        return self.src
    def get_dst_vnf(self):
        return self.dst

    def set_latency_request(self, latency_request):
        self.latency_request = latency_request
    def get_latency_request(self):
        return self.latency_request


if __name__ == '__main__':
    src_vnf = VNF('src')
    src_vnf.set_cpu_request(0)
    src_vnf.set_outcome_interface_banwdith(20)
    dst_vnf = VNF('dst')
    dst_vnf.set_cpu_request(0)
    sfc = SFC(src_vnf, dst_vnf)
    print sfc.get_number_of_vnfs()
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
    print sfc.get_number_of_vnfs()



