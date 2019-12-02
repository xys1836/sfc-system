import copy
import time
import ujson
"""
Consideration:
Algorithm should not do any modification on Substrate network/

It should only use network information and sfc information to 
solve and give out a mapping and route info, that

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
import logging
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
# ch = logging.StreamHandler()
ch = logging.FileHandler('./logs/DynamicProgrammingAlgorithm.log')
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')





class DynamicProgrammingAlgorithm():
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
        self.route_info = {}
        self.single_source_minimum_latency_path = None
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

    def clear_all(self):
        logger.debug('clear all')
        self.substrate_network = None
        self.sfc = None
        self.current_vnf = None
        self.next_vnf = None
        self.current_substrate_node = None
        self.node_info = {}
        self.src_substrate_node = None
        self.dst_substrate_node = None
        self.substrate_node_vnf_mapping = {} # {substrate_node_id: vnf_obj}
        self.route_info = {}
        self.single_source_minimum_latency_path = None

        self.copy_time = 0

    def install_substrate_network(self, substrate_network):
        # self.substrate_network = copy.deepcopy(substrate_network)
        self.substrate_network = substrate_network
        self.single_source_minimum_latency_path = self.substrate_network.pre_get_single_source_minimum_latency_path()
        self.substrate_network = copy.deepcopy(substrate_network)
        for node in self.substrate_network.nodes():
            self.substrate_network.nodes[node]['sfc_vnf_list']  = None

        return self.substrate_network

    def install_SFC(self, sfc):
        self.sfc = sfc

        src_vnf = self.sfc.get_src_vnf()
        src_substrate_node = self.sfc.get_substrate_node(src_vnf)
        dst_vnf = self.sfc.get_dst_vnf()
        dst_substrate_node = self.sfc.get_substrate_node(dst_vnf)

        for node in self.substrate_network.nodes():
            self.node_info[node] = {}
            for vnf_id, vnf in sfc.vnfs.items():
                self.node_info[node][vnf_id] = {}
                self.node_info[node][vnf_id]['flag'] = False  # This flag denote that whether vnf/id can be placed on node
                self.node_info[node][vnf_id]['latency'] = float('inf')
                self.node_info[node][vnf_id]['path'] = []
                self.node_info[node][vnf_id]['src_path'] = []
                self.node_info[node][vnf_id]['tmp_substrate_network'] = None
                self.node_info[node][vnf_id]['previous_substrate_node'] = None
                self.node_info[node][vnf_id]['current_substrate_nodes'] = []    # The meta information
                                                                                # in which is a set of substrate node
                                                                                # has been assigned to VNFs in order

            self.node_info[node][src_vnf.id] = {}
            self.node_info[node][src_vnf.id]['flag'] = False  # This means that src cannot be placed on the node except src node
            self.node_info[node][dst_vnf.id] = {}

        self.node_info[src_substrate_node][src_vnf.id]['flag'] = True # This means that src can be placed on the src node
        self.node_info[src_substrate_node][src_vnf.id]['tmp_substrate_network'] = self.get_copy_of_substrate_network()
        self.node_info[src_substrate_node][src_vnf.id]['latency'] = 0
        self.node_info[src_substrate_node][src_vnf.id]['src_path'] = [src_substrate_node]
        self.node_info[src_substrate_node][src_vnf.id]['path'] = []
        self.node_info[src_substrate_node][src_vnf.id]['current_substrate_nodes'] = [src_substrate_node]

        self.node_info[dst_substrate_node][dst_vnf.id]['flag'] = False
        self.node_info[dst_substrate_node][dst_vnf.id]['latency'] = float('inf')
        self.node_info[dst_substrate_node][dst_vnf.id]['src_path'] = []
        self.node_info[dst_substrate_node][dst_vnf.id]['path'] = []
        self.node_info[dst_substrate_node][dst_vnf.id]['tmp_substrate_network'] = None
        self.node_info[dst_substrate_node][dst_vnf.id]['current_substrate_nodes'] = []

        return self.sfc

    def start_algorithm(self):
        print "alg: start algorithm sfc:", self.sfc.id
        self.algorithm_new()
        print "alg: completed algorithm sfc:", self.sfc.id
        return

    def get_new_substrate_network(self):
        return self.substrate_network

    def get_new_sfc(self):
        return self.sfc

    def get_node_info(self):
        print "alg: get node info: sfc:", self.sfc.id
        return self.node_info

    def get_latency(self):
        return self.node_info[self.sfc.get_dst_vnf().get_substrate_node()]['dst']["latency"]


    def algorithm_new(self):
        print "random algorithm: "

        substrate_network = self.substrate_network
        sfc = self.sfc

        nodes = substrate_network.nodes()
        ## Get src and dst vnf
        src_vnf = sfc.get_src_vnf()
        dst_vnf = sfc.get_dst_vnf()

        ## Get substrate network nodes that src and dst are assigned in advanced
        src_substrate_node = sfc.get_substrate_node(src_vnf)
        dst_substrate_node = sfc.get_substrate_node(dst_vnf)

        self.src_substrate_node = src_substrate_node
        self.dst_substrate_node = dst_substrate_node

        
        vnf1 = src_vnf.get_next_vnf()
        self.dp(src_substrate_node, vnf1)


        vnf2 = vnf1.get_next_vnf()
        for node in nodes:
            self.dp(node, vnf2)

        # vnf3 = vnf2.get_next_vnf()
        # for node in nodes:
        #     self.dp(node, vnf3)
        
        # vnf4 = vnf3.get_next_vnf()
        # for node in nodes:
        #     self.dp(node, vnf4)
        
        # vnf5 = vnf4.get_next_vnf()
        # for node in nodes:
        #     self.dp(node, vnf5)

        # For dst:
        (node_latency, node_path) = self.single_source_minimum_latency_path[dst_substrate_node] # Get single source path from substrate node to all other substrate node
        # here node in latency and path results is the node host previous vnf
        previous_vnf = sfc.get_previous_vnf(dst_vnf)
        previous_vnf_id = previous_vnf.id
        for node, latency in node_latency.items():
            if node == dst_substrate_node or node == src_substrate_node:
                # if node is ingree or egree, continue
                continue
            _latency = self.node_info[node][previous_vnf_id]['latency']
            if not self.node_info[dst_substrate_node]['dst']['latency'] \
                or _latency + latency < self.node_info[dst_substrate_node]['dst']['latency']:
                self.node_info[dst_substrate_node]['dst']['latency'] = _latency + latency
                self.node_info[dst_substrate_node]['dst']['path'] = node_path[node]
                self.node_info[dst_substrate_node]['dst']['path'].reverse()
                self.node_info[dst_substrate_node]['dst']['current_substrate_nodes'] = self.node_info[node][previous_vnf_id]['current_substrate_nodes'][:]
                self.node_info[dst_substrate_node]['dst']['current_substrate_nodes'].append(dst_substrate_node) 
                self.node_info[dst_substrate_node]['dst']['src_path'] = self.node_info[node][previous_vnf_id]['src_path'][:] + self.node_info[dst_substrate_node]['dst']['path'][1:]
                


        print self.node_info


    def dp(self, substrate_node, vnf):
        """
        Start from substrate node substrate_node, calcuate all path and latency from substrate_node to other nodes N.
        update information in nodes N for vnf, if latency is minimum. 
        """
        ## Get precedent of the vnf
        sfc = self.sfc
        previous_vnf = sfc.get_previous_vnf(vnf)
        previous_vnf_id = previous_vnf.id
        if not self.node_info[substrate_node][previous_vnf_id]['flag']:
            ## this substrate node cannot host precedent vnf, thus, no need to exam further.
            return False
        
        vnf_id = vnf.id
        (node_latency, node_path) = self.single_source_minimum_latency_path[substrate_node] # Get single source path from substrate node to all other substrate node
        
        _latency = self.node_info[substrate_node][previous_vnf_id]['latency']

        cpu_request = sfc.get_vnf_cpu_request(vnf)
        bandwdith_request = self.substrate_network.get_link_bandwidth_free(e[0], e[1])

        for node, latency in node_latency.items():
            if node == substrate_node:
                ## cannot use the current substrate node to host this vnf.
                continue
            if node in self.node_info[substrate_node][previous_vnf_id]['current_substrate_nodes']:
                ## if node has been used, cannot host this vnf
                continue
            if node == self.src_substrate_node or node == self.dst_substrate_node:
                ## Ingress and egress cannot host this vnf
                continue

            # Check CPU resources
            cpu_available = self.substrate_network.get_node_cpu_free(node)
            if cpu_request > cpu_available:
                # if node has not sufficient cpu, check next node. 
                continue



            if not self.node_info[node][vnf_id]['latency'] or (_latency + latency) <= self.node_info[node][vnf_id]['latency']:
                self.node_info[node][vnf_id]['latency'] = _latency + latency
                self.node_info[node][vnf_id]['path'] = node_path[node]
                self.node_info[node][vnf_id]['flag'] = True
                self.node_info[node][vnf_id]['previous_substrate_node'] = substrate_node
                self.node_info[node][vnf_id]['current_substrate_nodes'] = self.node_info[substrate_node][previous_vnf_id]['current_substrate_nodes'][:]
                self.node_info[node][vnf_id]['current_substrate_nodes'].append(node) 

                self.node_info[node][vnf_id]['src_path'] = self.node_info[substrate_node][previous_vnf_id]['src_path'][:] + node_path[node][1:]
                



            

        
        








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
                # print "Checking dst node in vnf"
                break
        if all_failed_vnf:
            return None
        if not self.process_dst_vnf():
            return None

    def process_dst_vnf(self):
        # print "processing_dst_vnf"
        dst_vnf = self.sfc.get_dst_vnf()
        dst_substrate_node = self.sfc.get_substrate_node(dst_vnf)


        self.substrate_node_vnf_mapping[dst_substrate_node] = dst_vnf



        all_failed = True
        all_failed = self.iterate_substrate_node(dst_substrate_node, dst_vnf)
        if all_failed:
            self.process_no_sufficient_resources()
            print "in the dst phase"
            return
        self.route_info[dst_vnf.id] = []
        src_vnf = self.sfc.get_src_vnf()

        # previous_nfv = self.sfc.get_previous_vnf(dst_vnf)
        # previous_substrate_node = self.node_info[dst_substrate_node][dst_vnf.id]['previous_substrate_node']

        current_nfv = dst_vnf
        current_substrate_node = dst_substrate_node

        while current_nfv.id != src_vnf.id:
            previous_nfv = self.sfc.get_previous_vnf(current_nfv)
            current_substrate_node = self.sfc.get_substrate_node(current_nfv)
            previous_substrate_node = self.node_info[current_substrate_node][current_nfv.id]['previous_substrate_node']
            previous_nfv.assign_substrate_node(previous_substrate_node)
            # self.substrate_network.nodes[previous_substrate_node]['vnf_list'].append(previous_nfv)
            self.substrate_node_vnf_mapping[previous_substrate_node] = previous_nfv
            self.route_info[previous_nfv.id] = self.node_info[current_substrate_node][current_nfv.id]['path']
            self.route_info[previous_nfv.id].reverse()
            current_nfv = previous_nfv



        print ""

    def get_vnf_mapping(self):
        return self.substrate_node_vnf_mapping
    def get_route_info(self):
        print "alg: get route info: sfc:", self.sfc.id
        return self.route_info

    def process_no_sufficient_resources(self):
        print "No sufficient resources for provisioning SFC"

    def iterate_substrate_node(self, substrate_node, current_vnf):
        # (latency, paths) = self.substrate_network.get_single_source_minimum_latency_path(substrate_node)
        # (latency, paths) = self.substrate_network.get_single_source_minimum_latency_path_method(substrate_node)
        (latency, paths) = self.single_source_minimum_latency_path[substrate_node]
        # print latency
        # print paths
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
            # print node, path

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
            # print bandwidth_request
            # print bandwidth_free
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
                s1 = time.time()
                self.node_info[substrate_node][current_vnf.id]['tmp_substrate_network'] = copy.deepcopy(tmp_substrate_network)
                s = time.time()
                # print "copy substrate network: ", s - s1
                self.copy_time = self.copy_time + s - s1
                print self.copy_time
                tmp_path = self.node_info[node][previous_vnf.id]['src_path']
                tmp_path = copy.deepcopy(tmp_path)
                self.node_info[substrate_node][current_vnf.id]['path'] = copy.deepcopy(path)
                path = path[::-1]  # reverse the path, since the original path is starting from this substrate network to the one hosting previous vnf.
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




