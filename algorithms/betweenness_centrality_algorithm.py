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
ch = logging.FileHandler('./logs/RandomAlgorithm.log')
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

        bc = single_betweenness_centrality(substrate_network, src_substrate_node, dst_substrate_node, 'latency')
        path = substrate_network.get_shortest_path(src_substrate_node, dst_substrate_node)
        sorted_bc = sorted(bc.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        candidate_nodes = []
        for bc in sorted_bc:
            if bc[1] == 0:
                break
            if bc[0] in used_nodes:
                continue
            candidate_nodes.append(bc[0])
            used_nodes.append(bc[0])
        print candidate_nodes


        print bc

        used_nodes = [src_substrate_node, dst_substrate_node]
        map_res = {'src': src_substrate_node, 'dst': dst_substrate_node}
        vnf_list = ['src', 'vnf1', 'vnf2', 'vnf3', 'dst']
        def helper(substrate_network, vnf_list, head, tail, src, dst):
            # base condition
            print head, tail, src, dst
            if head < tail:
                middle_index = (tail - head) / 2 + head
                if vnf_list[middle_index] not in map_res:
                    bc = single_betweenness_centrality(substrate_network, src, dst, 'latency')
                    sorted_bc = sorted(bc.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
                    print sorted_bc
                    middle_vnf = vnf_list[middle_index]
                    candidate_node = None
                    count = 0
                    while True:
                        try:
                            candidate_node = sorted_bc[count][0]
                            if candidate_node not in used_nodes:
                                break
                            count += 1
                        except:
                            print "no node for host vnf"
                            return False
                    print candidate_node
                    map_res[middle_vnf] = candidate_node
                    used_nodes.append(candidate_node)
                    helper(substrate_network, vnf_list, head, middle_index, map_res[vnf_list[head]], map_res[vnf_list[middle_index]])
                    helper(substrate_network, vnf_list, middle_index, tail,  map_res[vnf_list[middle_index]], map_res[vnf_list[tail-1]])

        helper(substrate_network, vnf_list, 0, len(vnf_list), map_res[vnf_list[0]], map_res[vnf_list[len(vnf_list)-1]])
        print map_res





