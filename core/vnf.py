class Interface():
    def __init__(self, name):
        self.name = name
        self.bandwidth = 0
    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth

class VNFType():
    SRC = 0
    DST = 1
    TYPE1 = 2
    TYPE2 = 3
    TYPE3 = 4
    TYPE4 = 5

class VNF():

    def __init__(self, id):
        self.id = id
        self.cpu_request = None
        self.interfaces = {}
        self.previous_vnf = None   #todo: VNF should not keep the information of previous and next vnf.
                                   #todo: Previous and next vnf part should move to SFC and managed by SFC.
        self.next_vnf = None
        self.substrate_node = None
        self._attach_interfaces()
        self.type = None

    def _attach_interfaces(self):
        income_inf = Interface('income')
        outcome_inf = Interface('outcome')
        self.interfaces['income'] = income_inf
        self.interfaces['outcome'] = outcome_inf

    def set_cpu_request(self, amount):
        self.cpu_request = amount
    def get_cpu_request(self):
        return self.cpu_request

    def set_income_interface_bandwidth(self, request_bandwidth):
        self.interfaces['income'].set_bandwidth(request_bandwidth)

    def set_outcome_interface_bandwidth(self, request_bandwidth):
        self.interfaces['outcome'].set_bandwidth(request_bandwidth)

    def get_income_interface_bandwidth(self):
        return self.interfaces['income'].bandwidth
    def get_outcome_interface_bandwidth(self):
        return self.interfaces['outcome'].bandwidth

    def set_previous_vnf(self, vnf):
        self.previous_vnf = vnf
    def get_previous_vnf(self):
        return self.previous_vnf

    def set_next_vnf(self, vnf):
        self.next_vnf = vnf
    def get_next_vnf(self):
        return self.next_vnf

    def get_substrate_node(self):
        return self.substrate_node

    def assign_substrate_node(self, substrate_node):
        self.substrate_node = substrate_node

    def traffic_process(self, incoming):
        outcome = self.vnf_bw(incoming)
        self.set_outcome_interface_bandwidth(outcome)
        return outcome

    def vnf_function(self):
        incoming = self.get_income_interface_bandwidth()
        self.traffic_process(incoming)
        return self.get_outcome_interface_bandwidth()

    def vnf_bw(self, i):
        return i


if __name__ == '__main__':
    vnf = VNF('src')
    vnf.set_cpu_request(20)
    vnf.set_income_interface_bandwidth(20)
    vnf.set_outcome_interface_bandwidth(20)
    print vnf.get_income_interface_bandwidth()
    print vnf.get_outcome_interface_bandwidth()
    vnf.set_previous_vnf(vnf)
    vnf.set_next_vnf(vnf)
    print vnf.get_next_vnf().id
    print vnf.get_previous_vnf().id
