from core.vnf import VNF
# import networkx as nx
import json

class SFC():
    def __init__(self, vnf_src, vnf_dst):
        self.number_of_vnfs = 0 # This is not include src and dst
        self.vnfs = {} #This is not include src and dst
        self.src = vnf_src
        self.dst = vnf_dst
        self.link_bandwidth_dict = {}
        self.latency_request = 0
        self.id = None
        self.input_throughput = 0
        self.duration = 0
        self.arrival_time = 0
        self.depart_time = 0

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())

    def add_vnf(self, vnf):
        self.vnfs[vnf.id] = vnf
        self.number_of_vnfs += 1

    def remove_vnf(self, vnf):
        print "Remove vnf has not be realized! Exit"
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

    def change_link_bandwidth_request_to(self, vnf_id, bw):
        vnf = self.get_vnf_by_id(vnf_id)
        if not vnf.next_vnf:
            return
        next_vnf = vnf.next_vnf
        vnf.set_outcome_interface_bandwidth(bw)
        next_vnf.set_income_interface_bandwidth(bw)
        self.link_bandwidth_dict[(vnf.id, next_vnf.id)] = bw

    def change_node_cpu_request_to(self, vnf_id, cpu):
        vnf = self.get_vnf_by_id(vnf_id)
        vnf.set_cpu_request(cpu)

    def get_number_of_vnfs(self):
        return self.number_of_vnfs

    def get_vnf_cpu_request(self, vnf):
        return vnf.get_cpu_request()
    def get_link_bandwidth_request(self, vnf1_id, vnf2_id):
        if not vnf1_id or not vnf2_id:
            return 0
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
    def get_vnf_by_id(self, vnf_id):
        # This method could return the src and dst vnf
        if vnf_id == 'src':
            return self.src
        if vnf_id == 'dst':
            return self.dst
        return self.vnfs[vnf_id]

    def set_latency_request(self, latency_request):
        self.latency_request = latency_request
    def get_latency_request(self):
        return self.latency_request

    def set_input_throughput(self, tp):
        self.input_throughput = tp
        self.update()


    def update(self):
        if not self.input_throughput:
            return
        tp = self.input_throughput
        vnf = self.src
        vnf.set_income_interface_bandwidth(tp)

        while vnf.next_vnf:
            vnf.vnf_function()
            next_vnf = vnf.next_vnf
            link_bw = vnf.get_outcome_interface_bandwidth()
            next_vnf.set_income_interface_bandwidth(link_bw)
            self.link_bandwidth_dict[(vnf.id, next_vnf.id)] = link_bw
            vnf = next_vnf



    # def start(self):
    #     import thread
    #     print "sfc: " + str(self.id) + " START!"
    #     self.t = thread.start_new_thread(self.update, ())
    #
    # def stop(self):
    #     if self.t:
    #         print "sfc: " + str(self.id) + " STOP!"
    #         self.t.exit()




if __name__ == '__main__':
    src_vnf = VNF('src')
    src_vnf.set_cpu_request(0)
    src_vnf.set_outcome_interface_bandwidth(20)
    dst_vnf = VNF('dst')
    dst_vnf.set_cpu_request(0)
    sfc = SFC(src_vnf, dst_vnf)
    print sfc.get_number_of_vnfs()
    vnf1 = VNF(1)
    vnf1.set_cpu_request(10)
    vnf1.set_outcome_interface_bandwidth(10)
    vnf2 = VNF(2)
    vnf2.set_cpu_request(20)
    vnf2.set_outcome_interface_bandwidth(20)
    vnf3 = VNF(3)
    vnf3.set_cpu_request(30)
    vnf3.set_outcome_interface_bandwidth(30)
    sfc.add_vnf(vnf1)
    sfc.add_vnf(vnf2)
    sfc.add_vnf(vnf3)
    sfc.connect_two_vnfs(src_vnf, vnf1)
    sfc.connect_two_vnfs(vnf1, vnf2)
    sfc.connect_two_vnfs(vnf2, vnf3)
    sfc.connect_two_vnfs(vnf3, dst_vnf)
    print sfc.get_number_of_vnfs()



