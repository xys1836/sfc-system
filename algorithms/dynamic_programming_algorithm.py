import copy
import time

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
        self.name = "Dynamic Programming Algorithm"
        self.substrate_network = None
        self.sfc = None
        self.node_info = {}
        self.src_substrate_node = None
        self.dst_substrate_node = None
        self.route_info = {}
        self.single_source_minimum_latency_path = None
        self.latency = None

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
        '''

        pass

    def clear_all(self):
        logger.debug('clear all')
        self.substrate_network = None
        self.sfc = None
        self.node_info = {}
        self.src_substrate_node = None
        self.dst_substrate_node = None
        self.route_info = {}
        self.single_source_minimum_latency_path = None
        self.latency = None


    def install_substrate_network(self, substrate_network):
        self.substrate_network = substrate_network
        # self.single_source_minimum_latency_path = self.substrate_network.pre_get_single_source_minimum_latency_path()
        self.single_source_minimum_latency_path = self.substrate_network.single_source_minimum_latency_path


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
                # Not include src and dst.
                self.node_info[node][vnf_id] = {}
                self.node_info[node][vnf_id]['flag'] = False  # This flag denote that whether vnf/id can be placed on node
                self.node_info[node][vnf_id]['latency'] = float('inf')
                self.node_info[node][vnf_id]['path'] = []
                self.node_info[node][vnf_id]['src_path'] = []
                self.node_info[node][vnf_id]['previous_substrate_node'] = None
                self.node_info[node][vnf_id]['current_substrate_nodes'] = []    # The meta information
                                                                                # in which is a set of substrate node
                                                                                # has been assigned to VNFs in order
                self.node_info[node][vnf_id]['bandwidth_usage_info'] = {}

            self.node_info[node][src_vnf.id] = {}
            self.node_info[node][src_vnf.id]['flag'] = False  # This means that src cannot be placed on the node except src node
            self.node_info[node][dst_vnf.id] = {}


        self.node_info[src_substrate_node][src_vnf.id]['flag'] = True # This means that src can be placed on the src node
        self.node_info[src_substrate_node][src_vnf.id]['latency'] = 0
        # self.node_info[src_substrate_node][src_vnf.id]['src_path'] = [src_substrate_node]
        self.node_info[src_substrate_node][src_vnf.id]['src_path'] = []
        self.node_info[src_substrate_node][src_vnf.id]['path'] = []
        self.node_info[src_substrate_node][src_vnf.id]['current_substrate_nodes'] = [src_substrate_node]

        self.node_info[dst_substrate_node][dst_vnf.id]['flag'] = False
        self.node_info[dst_substrate_node][dst_vnf.id]['latency'] = float('inf')
        self.node_info[dst_substrate_node][dst_vnf.id]['src_path'] = []
        self.node_info[dst_substrate_node][dst_vnf.id]['path'] = []
        self.node_info[dst_substrate_node][dst_vnf.id]['current_substrate_nodes'] = []

        self.node_info[src_substrate_node][src_vnf.id]['bandwidth_usage_info'] = {}
        self.node_info[dst_substrate_node][dst_vnf.id]['bandwidth_usage_info'] = {}

        return self.sfc

    def get_latency(self):
        return self.latency

    def get_route_info(self):
        return self.route_info

    def start_algorithm(self):
        substrate_network = self.substrate_network
        sfc = self.sfc
        logger.info('Algorithm start')
        if self.algorithm(substrate_network, sfc):
            logger.info('Algorithm end, success')
            return True
        logger.info('Algorithm end, failed')
        return False


    def get_new_substrate_network(self):
        return self.substrate_network

    def get_new_sfc(self):
        return self.sfc

    def algorithm(self,substrate_network, sfc):
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

        vnf = vnf1.get_next_vnf()
        while vnf.id != dst_vnf.id:
            for node in nodes:
                self.dp(node, vnf)
            vnf = vnf.get_next_vnf()

        # For dst:
        (node_latency, node_path) = self.single_source_minimum_latency_path[dst_substrate_node] # Get single source path from substrate node to all other substrate node
        # here node in latency and path results is the node host previous vnf
        previous_vnf = sfc.get_previous_vnf(dst_vnf)
        previous_vnf_id = previous_vnf.id

        bandwidth_request = sfc.get_link_bandwidth_request(previous_vnf_id, dst_vnf.id)

        for node, latency in node_latency.items():
            if node == dst_substrate_node or node == src_substrate_node:
                # if node is ingress or egress, continue
                continue

            # Check bandwidth resources
            is_bandwidth_sufficient = True
            bandwidth_usage_info = copy.copy(
                self.node_info[node][previous_vnf_id]['bandwidth_usage_info'])
            path = node_path[node]
            length = len(path)
            for i in range(0, length - 1):
                edge_key = frozenset((path[i], path[i + 1]))
                residual_bandwidth = None
                if edge_key in bandwidth_usage_info:
                    residual_bandwidth = bandwidth_usage_info[edge_key] - bandwidth_request
                else:
                    residual_bandwidth = self.substrate_network.get_link_bandwidth_free(path[i],
                                                                                        path[i + 1]) - bandwidth_request
                if residual_bandwidth < 0:
                    logger.warning('Bandwidth resources is not sufficient to dst')
                    is_bandwidth_sufficient = False
                    break
                bandwidth_usage_info[edge_key] = residual_bandwidth
            if not is_bandwidth_sufficient:
                # check next path
                continue

            _latency = self.node_info[node][previous_vnf_id]['latency']
            if not self.node_info[dst_substrate_node][dst_vnf.id]['latency'] \
                or _latency + latency < self.node_info[dst_substrate_node][dst_vnf.id]['latency']:
                self.node_info[dst_substrate_node][dst_vnf.id]['latency'] = _latency + latency
                self.node_info[dst_substrate_node][dst_vnf.id]['path'] = node_path[node]
                self.node_info[dst_substrate_node][dst_vnf.id]['path'].reverse()
                self.node_info[dst_substrate_node][dst_vnf.id]['current_substrate_nodes'] = self.node_info[node][previous_vnf_id]['current_substrate_nodes'][:]
                self.node_info[dst_substrate_node][dst_vnf.id]['current_substrate_nodes'].append(dst_substrate_node)
                self.node_info[dst_substrate_node][dst_vnf.id]['src_path'] = self.node_info[node][previous_vnf_id]['src_path'][:] + self.node_info[dst_substrate_node]['dst']['path'][:]
                self.node_info[dst_substrate_node][dst_vnf.id]['flag'] = True

        if self.node_info[dst_substrate_node][dst_vnf.id]['flag']:
            # there is a solution
            # Backtracking
            # TODO: form route_info

            # start from dst to backtracking to src
            previous_vnf = dst_vnf
            previous_substrate_node = dst_substrate_node
            while True:

                path = self.node_info[previous_substrate_node][previous_vnf.id]['path']
                if not path:
                    break
                previous_substrate_node = path[0]
                previous_vnf = sfc.get_previous_vnf(previous_vnf)
                if previous_vnf:
                    self.route_info[previous_vnf.id] = path
                else:
                    break
            self.route_info[dst_vnf.id] = []
            self.latency = self.node_info[dst_substrate_node][dst_vnf.id]['latency']
            return True
        else:
            return False


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
        bandwidth_request = sfc.get_link_bandwidth_request(previous_vnf_id, vnf_id)

        for node, latency in node_latency.items():
            if node == substrate_node:
                ## cannot use the current substrate node to host this vnf.
                continue
            if node in self.node_info[substrate_node][previous_vnf_id]['current_substrate_nodes']:
                ## if node has been used, cannot host this vnf
                # current_substrate_nodes contains the nodes that have been used
                continue
            if node == self.src_substrate_node or node == self.dst_substrate_node:
                ## Ingress and egress cannot host this vnf
                continue

            # Check CPU resources
            cpu_available = self.substrate_network.get_node_cpu_free(node)
            if cpu_request > cpu_available:
                # if node has not sufficient cpu, check next node. 
                continue

            # Check bandwidth resources
            is_bandwidth_sufficient = True
            bandwidth_usage_info = copy.copy(
                self.node_info[substrate_node][previous_vnf_id]['bandwidth_usage_info'])
            path = node_path[node]
            length = len(path)
            for i in range(0, length - 1):
                edge_key = frozenset((path[i], path[i + 1]))
                residual_bandwidth = None
                if edge_key in bandwidth_usage_info:
                    residual_bandwidth = bandwidth_usage_info[edge_key] - bandwidth_request
                else:
                    residual_bandwidth = self.substrate_network.get_link_bandwidth_free(path[i],
                                                                                        path[i + 1]) - bandwidth_request
                if residual_bandwidth < 0:
                    logger.warning('Bandwidth resources is not sufficient')
                    is_bandwidth_sufficient = False
                    break
                bandwidth_usage_info[edge_key] = residual_bandwidth
            if not is_bandwidth_sufficient:
                continue
            self.node_info[node][vnf_id]['bandwidth_usage_info'] = bandwidth_usage_info

            if not self.node_info[node][vnf_id]['latency'] or (_latency + latency) <= self.node_info[node][vnf_id]['latency']:
                self.node_info[node][vnf_id]['latency'] = _latency + latency
                self.node_info[node][vnf_id]['path'] = node_path[node]
                self.node_info[node][vnf_id]['flag'] = True
                self.node_info[node][vnf_id]['previous_substrate_node'] = substrate_node
                self.node_info[node][vnf_id]['current_substrate_nodes'] = self.node_info[substrate_node][previous_vnf_id]['current_substrate_nodes'][:]
                self.node_info[node][vnf_id]['current_substrate_nodes'].append(node)
                self.node_info[node][vnf_id]['src_path'] = self.node_info[substrate_node][previous_vnf_id]['src_path'][:] + node_path[node][:-1]



            

        
        




