class SubstrateNetworkController():
    pass
    def __init__(self, nw):
        pass
        self.substrate_network = nw
        self.node_info = {}
        self.alg = None
        self.sfc_list = []

    def output_nodes_information(self):
        self.substrate_network.print_out_nodes_information()

    def output_edges_information(self):
        self.substrate_network.print_out_edges_information()

    def get_nodes_information(self):
        for node in self.substrate_network.nodes():
            self.node_info[node] = self.get_node_information(node)

    def get_node_information(self, node_id):
        cpu_used = self.substrate_network.get_node_cpu_used(node_id)
        cpu_free = self.substrate_network.get_node_cpu_free(node_id)
        cpu_capacity = self.substrate_network.get_node_cpu_capacity(node_id)
        sfc_vnf_list = self.substrate_network.get_node_sfc_vnf_list(node_id)
        return (cpu_used, cpu_free, cpu_capacity, sfc_vnf_list)

    def update(self):
        self.substrate_network.update()
        self.get_nodes_information()


    def deploy_sfc(self, sfc, alg):
        if sfc.id in self.sfc_list:
            print "sfc has been deployed"
            return
        alg.install_substrate_network(self.substrate_network)
        alg.install_SFC(sfc)
        alg.start_algorithm()
        route_info = alg.get_route_info()
        self.substrate_network.deploy_sfc(sfc, route_info)
        self.sfc_list.append(sfc.id)