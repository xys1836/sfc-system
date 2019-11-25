import copy
import random

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
ch = logging.FileHandler('./logs/RandomAlgorithm.log')
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





class RandomAlgorithm():
    def __init__(self):
        self.substrate_network = None
        self.sfc = None
        self.node_info = None
        self.route_info = None
        self.latency = None


    def clear_all(self):
        print "random algorithm: clear all"
        self.substrate_network = None
        self.sfc = None
        self.node_info = None
        self.route_info = None
        self.latency = None

    def install_substrate_network(self, substrate_network):
        self.substrate_network = copy.deepcopy(substrate_network)
        return self.substrate_network

    def install_SFC(self, sfc):
        self.sfc = sfc
        # src_vnf = self.sfc.get_src_vnf()
        # src_substrate_node = self.sfc.get_substrate_node(src_vnf)
        # self.src_substrate_node = src_substrate_node
        # dst_vnf = self.sfc.get_dst_vnf()
        # dst_substrate_node = self.sfc.get_substrate_node(dst_vnf)
        # self.dst_substrate_node = dst_substrate_node

        return self.sfc

    def start_algorithm(self):
        substrate_network = self.substrate_network
        sfc = self.sfc
        self.algorithm(substrate_network, sfc)
        return

    # def get_node_info(self):
    #     return self.node_info

    def get_latency(self):
        return self.latency
    
    def get_route_info(self):
        return self.route_info

    def algorithm(self, substrate_network, sfc):

        print "random algorithm: "

        nodes = substrate_network.nodes()
        ## Get src and dst vnf
        src_vnf = sfc.get_src_vnf()
        dst_vnf = sfc.get_dst_vnf()

        ## Get substrate network nodes that src and dst are assigned in advanced
        src_substrate_node = sfc.get_substrate_node(src_vnf)
        dst_substrate_node = sfc.get_substrate_node(dst_vnf)

        number_of_vnfs = sfc.get_number_of_vnfs()

        nodesList = list(nodes)
        nodesList.remove(src_substrate_node)
        print nodesList

        
        random_sampled_substrate_network_nodes = random.sample(nodesList, k=number_of_vnfs)
        random_sampled_substrate_network_nodes.append(dst_substrate_node)

        route_info = {}
        current_vnf = src_vnf
        count = 0
        pre_substrate_node = src_substrate_node
        latency = 0
        for node in random_sampled_substrate_network_nodes:
            path_length = substrate_network.get_shortest_path_length(pre_substrate_node, node)
            path = substrate_network.get_shortest_path(pre_substrate_node, node)
            pre_substrate_node = node

            latency = latency + path_length
            vnf_id = current_vnf.id
            route_info[vnf_id] = path
            current_vnf = current_vnf.get_next_vnf()

            cpu_request = sfc.get_vnf_cpu_request(current_vnf)
            cpu_available = substrate_network.get_node_cpu_free(node)

            if cpu_request > cpu_available:
                print "cpu resources is not sufficient"
                return False

            bandwidth_request = sfc.get_link_bandwidth_request(vnf_id, current_vnf.id)
            bandwidth_available = substrate_network.get_minimum_free_bandwidth(path)

            if bandwidth_request > bandwidth_available :
                print "bandwidth resources is not sufficient"
                return False


        route_info['dst'] = []  # make a placeholder for dst.
        self.route_info = route_info
        self.latency = latency
        return True
