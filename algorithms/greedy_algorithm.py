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
ch = logging.FileHandler('./logs/GreedyAlgorithm.log')
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





class GreedyAlgorithm():
    def __init__(self):
        self.name = "Greedy Algorithm"
        self.substrate_network = None
        self.sfc = None
        self.node_info = None
        self.route_info = None
        self.latency = None


    def clear_all(self):
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
        return self.sfc

    def start_algorithm(self):
        substrate_network = self.substrate_network
        sfc = self.sfc
        logger.info("Start algorithm")
        if self.algorithm(substrate_network, sfc):
            logger.info("End algorithm, success")
            return True
        logger.info("End algorithm, failed")
        return False

    def get_latency(self):
        return self.latency
    
    def get_route_info(self):
        return self.route_info

    def algorithm(self, substrate_network, sfc):
        ## Get src and dst vnf
        src_vnf = sfc.get_src_vnf()
        dst_vnf = sfc.get_dst_vnf()

        ## Get substrate network nodes that src and dst are assigned in advanced
        src_substrate_node = sfc.get_substrate_node(src_vnf)
        dst_substrate_node = sfc.get_substrate_node(dst_vnf)

        route_info = {}
        bandwidth_usage_info = {}
        node = None
        latency = 0
        used_node = [src_substrate_node, dst_substrate_node]

        number_of_vnfs = sfc.get_number_of_vnfs()
        current_vnf = src_vnf
        current_substrate_node = src_substrate_node
        for i in range(0, number_of_vnfs):
            
            edges = substrate_network.edges(current_substrate_node)
            next_vnf = current_vnf.get_next_vnf()

            cpu_request = sfc.get_vnf_cpu_request(next_vnf)
            bandwidth_request = sfc.get_link_bandwidth_request(current_vnf.id, next_vnf.id)

            min_latency = None
            
            for e in edges:
                logger.debug(e)
                if e[1] in used_node:
                    # do not use the node used before, to avoid loop
                    logger.debug("-----------------------------> node %s have been used", e[1])
                    continue
                cpu_available = substrate_network.get_node_cpu_free(e[1])
                if cpu_request > cpu_available:
                    # if node has not sufficient cpu, check next edge.
                    logger.debug("node %s has not sufficient cpu", e[1])
                    continue

                bandwidth_available = substrate_network.get_link_bandwidth_free(e[0], e[1])
                if bandwidth_request > bandwidth_available:
                    # if edge has not sufficient bandwidth, check next edge.
                    logger.debug("edge has not sufficient bandwidth, check next edge")
                    continue
                
                edge_latency = substrate_network.get_link_latency(e[0], e[1])
                if not min_latency or edge_latency < min_latency:
                    logger.debug("-----------------------------> node %s have minimum latency", e[1])
                    min_latency = edge_latency
                    node = e[1]

            if node != None:
                # be careful that node can be 0
                route_info[current_vnf.id] = [current_substrate_node, node]
                used_node.append(node)
                latency = latency + min_latency

                edge_key = frozenset((current_substrate_node, node))

                # Record the bandwidth usage in bandwidth_usage_info
                residual_bandwidth = None
                if edge_key in bandwidth_usage_info:
                    residual_bandwidth = bandwidth_usage_info[edge_key] - bandwidth_request
                else:
                    residual_bandwidth = substrate_network.get_link_bandwidth_free(current_substrate_node,
                                                                                   node) - bandwidth_request
                if residual_bandwidth < 0:
                    logger.warning('Bandwidth resources is not sufficient')
                    return False
                bandwidth_usage_info[edge_key] = residual_bandwidth


            else:
                logger.debug("node is not existing")
                return False
            
            current_substrate_node = node
            current_vnf = next_vnf
            # route_info[current_vnf.id] = []
        

        try:
            path = substrate_network.get_shortest_path(node, dst_substrate_node)
            path_latency = substrate_network.get_shortest_path_length(node, dst_substrate_node)
        except:
            logger.warning('have no path between last vnf and dst: %s - %s', node, dst_substrate_node)
            return False
        
        bandwidth_request = sfc.get_link_bandwidth_request(current_vnf.id, 'dst')
        bandwidth_available = substrate_network.get_minimum_free_bandwidth(path)

        length = len(path)
        for i in range(0, length - 1):
            edge_key = frozenset((path[i], path[i + 1]))
            residual_bandwidth = None
            if edge_key in bandwidth_usage_info:
                residual_bandwidth = bandwidth_usage_info[edge_key] - bandwidth_request
            else:
                residual_bandwidth = substrate_network.get_link_bandwidth_free(path[i],
                                                                               path[i + 1]) - bandwidth_request
            if residual_bandwidth < 0:
                logger.warning('Bandwidth resources is not sufficient')
                return False
            bandwidth_usage_info[edge_key] = residual_bandwidth




        if bandwidth_request > bandwidth_available:
            # if edge has not sufficient bandwidth, check next edge. 
            return False


        route_info[current_vnf.id] = path
        route_info['dst'] = []
        latency = latency + path_latency


        self.route_info = route_info
        self.latency = latency

        return True
