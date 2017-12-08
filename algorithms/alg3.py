import copy


"""
Consideration:
Algorithm should not do any modification on Substrate network/

It should only use network information and sfc information to 
solve and give out a mapping and routing info, that

sfc_id: 
{substrate_node_id <- vnf_id}
<- is a mapping

sfc_id:
{
    src:  [1, 2, 3],
    vnf1: [3, 4, 5],
    vnf2: [5, 6, 7],
    vnf3: [7, 8 ,9],
    dst:  []

}


"""

class ALG3():
    def __init__(self):
        self.substrate_network = None
        self.sfc = None
        self.current_vnf = None
        self.next_vnf = None
        self.current_substrate_node = None
        self.node_info = {}
        self.src_substrate_node = None
        self.dst_substrate_node = None
        self.substrate_node_vnf_mapping = {} # {substrate_node_id: vnf_obj}
        self.routing_info = {}
        # self.all_pair_shortest_path_dict = {}
        '''
        node info
        latency: 
        path:
        number of nodes on path:
        mini bandwidth: ?

        node:{vnf_id: {latency:0, path:[], flag:True}}

        node_info[node][vnf_id][latency]
        node_info[node][vnf_id][path]
        node_info[node][vnf_id][flag]
        node_info[node][vnf_id][tmp_substrate_network]
        '''

        pass

    def install_substrate_network(self, substrate_network):
        # self.substrate_network = copy.deepcopy(substrate_network)
        self.substrate_network = substrate_network

        # for node in substrate_network.nodes():
        #     self.node_info[node] = {}
        return self.substrate_network

    def install_SFC(self, sfc):
        # self.sfc = copy.deepcopy(sfc)
        self.sfc = sfc
        src_vnf = self.sfc.get_src_vnf()
        src_substrate_node = self.sfc.get_substrate_node(src_vnf)
        self.src_substrate_node = src_substrate_node
        dst_vnf = self.sfc.get_dst_vnf()
        dst_substrate_node = self.sfc.get_substrate_node(dst_vnf)
        self.dst_substrate_node = dst_substrate_node

        for node in self.substrate_network.nodes():
            self.node_info[node] = {}
            for vnf_id, vnf in self.sfc.vnfs.items():
                self.node_info[node][vnf_id] = {}
                self.node_info[node][vnf_id][
                    'flag'] = False  # This flag denote that whether vnf/id can be placed on node
                self.node_info[node][vnf_id]['latency'] = float('inf')
                self.node_info[node][vnf_id]['path'] = []
                self.node_info[node][vnf_id]['src_path'] = []
                self.node_info[node][vnf_id]['tmp_substrate_network'] = None
                self.node_info[node][vnf_id]['previous_substrate_node'] = None
                self.node_info[node][vnf_id]['current_substrate_nodes'] = []    # The meta information
                                                                                # in which is a set of substrate node
                                                                                # has been assigned to VNFs in order

            self.node_info[node][src_vnf.id] = {}
            self.node_info[node][src_vnf.id]['flag'] = False  # This means that src can be placed on the src node
            self.node_info[node][dst_vnf.id] = {}

        self.node_info[src_substrate_node][src_vnf.id]['flag'] = True
        self.node_info[src_substrate_node][src_vnf.id]['tmp_substrate_network'] = self.get_copy_of_substrate_network()
        self.node_info[src_substrate_node][src_vnf.id]['latency'] = 0
        self.node_info[src_substrate_node][src_vnf.id]['src_path'] = [src_substrate_node]
        self.node_info[src_substrate_node][src_vnf.id]['path'] = []
        self.node_info[src_substrate_node][src_vnf.id]['current_substrate_nodes'] = [1]

        self.node_info[dst_substrate_node][dst_vnf.id]['flag'] = False
        self.node_info[dst_substrate_node][dst_vnf.id]['latency'] = float('inf')
        self.node_info[dst_substrate_node][dst_vnf.id]['src_path'] = []
        self.node_info[dst_substrate_node][dst_vnf.id]['path'] = []
        self.node_info[dst_substrate_node][dst_vnf.id]['tmp_substrate_network'] = None
        self.node_info[dst_substrate_node][dst_vnf.id]['current_substrate_nodes'] = []

        return self.sfc

    def start_algorithm(self):
        self.algorithm()
        return

    def get_new_substrate_network(self):
        return self.substrate_network

    def get_new_sfc(self):
        return self.sfc

    def algorithm(self):
        src = self.sfc.get_src_vnf()
        current_vnf = self.sfc.get_next_vnf(src)
        all_failed_vnf = True
        while current_vnf:
            for node in self.substrate_network.nodes():
                all_failed = self.iterate_substrate_node(node, current_vnf)
                if not all_failed:
                    all_failed_vnf = False
            if all_failed_vnf:
                self.process_no_sufficient_resources()
                break
            current_vnf = self.sfc.get_next_vnf(current_vnf)
            if current_vnf.id == 'dst':
                print "Checking dst node in vnf"
                break
        self.process_dst_vnf()

    def process_dst_vnf(self):
        print "processing_dst_vnf"
        dst_vnf = self.sfc.get_dst_vnf()
        dst_substrate_node = self.sfc.get_substrate_node(dst_vnf)


        self.substrate_node_vnf_mapping[dst_substrate_node] = dst_vnf
        self.routing_info[dst_vnf.id] = []


        all_failed = True
        all_failed = self.iterate_substrate_node(dst_substrate_node, dst_vnf)
        if all_failed:
            self.process_no_sufficient_resources()
        src_vnf = self.sfc.get_src_vnf()
        # self.substrate_network = self.node_info[dst_substrate_node][dst_vnf.id]['tmp_substrate_network']

        previous_nfv = self.sfc.get_previous_vnf(dst_vnf)
        previous_substrate_node = self.node_info[dst_substrate_node][dst_vnf.id]['previous_substrate_node']
        # previous_substrate_node = dst_substrate_node

        current_nfv = dst_vnf
        current_substrate_node = dst_substrate_node

        # previous_nfv = self.sfc.get_previous_vnf(current_nfv)
        # previous_substrate_node = self.node_info[current_substrate_node][current_nfv.id]['previous_substrate_node']
        # previous_nfv.assign_substrate_node(previous_substrate_node)



        while current_nfv.id != src_vnf.id:
            previous_nfv = self.sfc.get_previous_vnf(current_nfv)
            current_substrate_node = self.sfc.get_substrate_node(current_nfv)
            previous_substrate_node = self.node_info[current_substrate_node][current_nfv.id]['previous_substrate_node']
            previous_nfv.assign_substrate_node(previous_substrate_node)
            # self.substrate_network.nodes[previous_substrate_node]['vnf_list'].append(previous_nfv)
            self.substrate_node_vnf_mapping[previous_substrate_node] = previous_nfv
            self.routing_info[previous_nfv.id] = self.node_info[current_substrate_node][current_nfv.id]['path']
            self.routing_info[previous_nfv.id].reverse()
            current_nfv = previous_nfv



        print ""

    def get_vnf_mapping(self):
        return self.substrate_node_vnf_mapping
    def get_routing_info(self):
        return self.routing_info

    def process_no_sufficient_resources(self):
        print "No sufficient resources for provisioning SFC"

    def iterate_substrate_node(self, substrate_node, current_vnf):
        (latency, paths) = self.substrate_network.get_single_source_minimum_latency_path(substrate_node)
        print latency
        print paths
        # Here should be carefully considered
        # del latency[substrate_node]
        # del paths[substrate_node]

        previous_vnf = self.sfc.get_previous_vnf(current_vnf)
        all_failed = True
        if not previous_vnf:
            print "no previous VNF"
            return
        minimum_latency_path = None
        cpu_request = 0
        bandwidth_request = 0

        for node, path in paths.items():
            print node, path

            if not self.node_info[node][previous_vnf.id]['flag']:
                continue
            if substrate_node in self.node_info[node][previous_vnf.id]['current_substrate_nodes']:
                # this node has been used before
                continue
            tmp_substrate_network = self.node_info[node][previous_vnf.id]['tmp_substrate_network']
            if not tmp_substrate_network:
                tmp_substrate_network = self.get_copy_of_substrate_network()
                # if we assigned a copy of substrate network to src, here should never be executed.
            bandwidth_request = self.sfc.get_link_bandwidth_request(previous_vnf.id, current_vnf.id)
            bandwidth_free = tmp_substrate_network.get_minimum_free_bandwidth(path)
            print bandwidth_request
            print bandwidth_free
            if bandwidth_free < bandwidth_request:
                continue
            cpu_request = self.sfc.get_vnf_cpu_request(current_vnf)
            cpu_free = tmp_substrate_network.get_node_cpu_free(substrate_node)
            if cpu_free < cpu_request:
                continue

            # CPU and Bandwidth resources are sufficient
            # Set this node flag True which mean this node could host this vnf
            # Calculate the latency from src to this node through all the vnfs
            # append the node to the path.
            current_node_latency = self.node_info[node][previous_vnf.id]['latency'] + latency[node]
            if current_node_latency <= self.node_info[substrate_node][current_vnf.id]['latency']:
                minimum_latency_path = path
                self.node_info[substrate_node][current_vnf.id]['latency'] = current_node_latency
                self.node_info[substrate_node][current_vnf.id]['flag'] = True
                self.node_info[substrate_node][current_vnf.id]['tmp_substrate_network'] = copy.deepcopy(
                    tmp_substrate_network)
                tmp_path = self.node_info[node][previous_vnf.id]['src_path']
                tmp_path = copy.deepcopy(tmp_path)
                self.node_info[substrate_node][current_vnf.id]['path'] = copy.deepcopy(path)
                path = path[
                       ::-1]  # reverse the path, since the original path is starting from this substrate network to the one hosting previous vnf.
                for n in path[1:]:  # Do not count the node hosting previous vnf twice.
                    tmp_path.append(n)
                self.node_info[substrate_node][current_vnf.id]['src_path'] = tmp_path[:]
                self.node_info[substrate_node][current_vnf.id]['previous_substrate_node'] = node

                self.node_info[substrate_node][current_vnf.id]['current_substrate_nodes'] = \
                self.node_info[node][previous_vnf.id]['current_substrate_nodes'][:]
                self.node_info[substrate_node][current_vnf.id]['current_substrate_nodes'].append(substrate_node)

            all_failed = False

        if minimum_latency_path:
            self.node_info[substrate_node][current_vnf.id]['tmp_substrate_network'].allocate_cpu_resource(
                substrate_node, cpu_request)
            self.node_info[substrate_node][current_vnf.id]['tmp_substrate_network'].allocate_bandwidth_resource_path(
                minimum_latency_path, bandwidth_request)

        return all_failed

    def get_copy_of_substrate_network(self):
        return copy.deepcopy(self.substrate_network)

    def make_a_copy_of_network(self, network):
        return copy.deepcopy(network)




