"""
Consideration:
Algorithm should not do any modification on substrate network

It should only use network information and sfc information to
solve and give out a mapping and route info, that

route info :=
{
    src:  [1, 2, 3],
    vnf1: [3, 4, 5],
    vnf2: [5, 6, 7],
    vnf3: [7, 8 ,9],
    dst:  []
}

"""
import logging
from utils.betweenness_centrality import single_betweenness_centrality
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
# ch = logging.StreamHandler()
from config import ROOT_PATH
ch = logging.FileHandler(ROOT_PATH + './logs/BetweennessCentralityAlgorithm.log')
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class BetweennessCentralityAlgorithm():
    def __init__(self):
        self.name = "Betweenness Centrality Algorithm"
        self.substrate_network = None
        self.sfc = None
        self.node_info = None
        self.route_info = None
        self.latency = None

    def clear_all(self):
        logger.info('clear all')
        self.substrate_network = None
        self.sfc = None
        self.node_info = None
        self.route_info = None
        self.latency = None

    def install_substrate_network(self, substrate_network):
        self.substrate_network = substrate_network
        return self.substrate_network

    def install_SFC(self, sfc):
        self.sfc = sfc
        return self.sfc

    def start_algorithm(self):
        substrate_network = self.substrate_network
        sfc = self.sfc
        logger.info('Algorithm start')
        if self.algorithm(substrate_network, sfc):
            logger.info('Algorithm end, success')
            return True
        logger.info('Algorithm end, failed')
        return False

    def get_latency(self):
        return self.latency

    def get_route_info(self):
        return self.route_info

    def algorithm(self, substrate_network, sfc):
        nodes = substrate_network.nodes()
        ## Get src and dst vnf
        src_vnf = sfc.get_src_vnf()
        dst_vnf = sfc.get_dst_vnf()

        # Get substrate network nodes that src and dst are assigned in advanced
        # (ingress and egress substrate network nodes)
        src_substrate_node = sfc.get_substrate_node(src_vnf)
        dst_substrate_node = sfc.get_substrate_node(dst_vnf)

        number_of_vnfs = sfc.get_number_of_vnfs()

        used_nodes = [src_substrate_node, dst_substrate_node]
        map_res = {'src': src_substrate_node, 'dst': dst_substrate_node}
        vnf_list = []

        current_vnf = src_vnf
        while current_vnf:
            vnf_list.append(current_vnf)
            current_vnf = sfc.get_next_vnf(current_vnf)

        # print vnf_list
        def helper(substrate_network, sfc, vnf_list, head, tail, src, dst):
            # base condition
            # print "------------------------------------",head, tail, src, dst
            if head < tail:
                middle_index = (tail - head) / 2 + head
                if vnf_list[middle_index].id not in map_res:
                    bc = single_betweenness_centrality(substrate_network, src, dst, 'latency')
                    sorted_bc = sorted(bc.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
                    # print sorted_bc
                    middle_vnf = vnf_list[middle_index]
                    candidate_node = None
                    count = 0


                    # check cpu resource
                    cpu_request = sfc.get_vnf_cpu_request(middle_vnf)


                    while True:
                        try:
                            candidate_node = sorted_bc[count][0]
                            cpu_available = substrate_network.get_node_cpu_free(candidate_node)
                            if candidate_node not in used_nodes and cpu_available >= cpu_request:
                                break
                            count += 1
                        except:
                            print "no node for host vnf"
                            return False
                    # print candidate_node
                    map_res[middle_vnf.id] = candidate_node
                    used_nodes.append(candidate_node)
                    helper(substrate_network, sfc, vnf_list, head, middle_index, map_res[vnf_list[head].id], map_res[vnf_list[middle_index].id])
                    helper(substrate_network, sfc, vnf_list, middle_index, tail,  map_res[vnf_list[middle_index].id], map_res[vnf_list[tail].id])

        helper(substrate_network, sfc, vnf_list, 0, len(vnf_list)-1, map_res[vnf_list[0].id], map_res[vnf_list[len(vnf_list)-1].id])

        # TODO: find shortest path between vnfs

        current_vnf = src_vnf
        next_vnf = sfc.get_next_vnf(current_vnf)
        route_info = {}
        bandwidth_usage_info = {}
        latency = 0
        while next_vnf:
            node_from = map_res[current_vnf.id]
            node_to = map_res[next_vnf.id]
            try:
                path = substrate_network.get_shortest_path(node_from, node_to)
            except:
                logger.warning('No shortest path')
                return False
            path_latency = substrate_network.get_shortest_path_length(node_from, node_to)
            latency = latency + path_latency
            bandwidth_request = sfc.get_link_bandwidth_request(current_vnf.id, next_vnf.id)

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
                    print 'bandwidth resource is not sufficient'
                    return False
                bandwidth_usage_info[edge_key] = residual_bandwidth


            route_info[current_vnf.id] = path
            current_vnf = next_vnf
            next_vnf = sfc.get_next_vnf(next_vnf)


        route_info[dst_vnf.id] = []

        self.route_info = route_info
        self.latency = latency
        return True



