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
from utils.k_shortest_paths import k_shortest_paths
import logging
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
# ch = logging.StreamHandler()
from config import ROOT_PATH
ch = logging.FileHandler(ROOT_PATH + './logs/KShortestAlgorithm.log')
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class KShortestPathsAlgorithm():
    '''k-shortest paths algorithm.
    Find k shortest paths between src and dst.
    Use the longest path as the candidate path. (initial path, who has the most number of node along the path)
    If the number of nodes along the path cannot host all the VNFs in the SFC,
    find the edge with least available bandwidth resource, say edge (m,n).
    Remove the edge (m,n) from the path.
    Check and compare the CPU capacity of m's neighbor nodes and n's neighbor.
    Select the node who has the most available CPU capacity to host VNF, say node c.
    Find the shortest paths from c to m, and c to n.

    Refer to the following paper.

    L. Qu, C. Assi, K. Shaban, and M. J. Khabbaz, "A reliability-aware network service chain provisioning with delay guarantees in NFV-enabled enterprise datacenter networks," IEEE Trans. Netw. Service Manag.,vol. 14, no. 3, pp. 554-568, Sep. 2017.
    '''
    def __init__(self, k):
        self.name = "k shortest paths algorithm"
        self.substrate_network = None
        self.sfc = None
        self.node_info = None
        self.route_info = None
        self.latency = None
        self.k = k


    def clear_all(self):
        logger.debug('clear all')
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
        k = self.k

        ## Get src and dst vnf
        src_vnf = sfc.get_src_vnf()
        dst_vnf = sfc.get_dst_vnf()

        ## Get substrate network nodes that src and dst are assigned in advanced
        src_substrate_node = sfc.get_substrate_node(src_vnf)
        dst_substrate_node = sfc.get_substrate_node(dst_vnf)

        number_of_vnfs = sfc.get_number_of_vnfs()

        used_node = [src_substrate_node, dst_substrate_node]

        k_shortest_paths_res = k_shortest_paths(substrate_network, src_substrate_node, dst_substrate_node, k, 'latency')

        # find the longest single path ip:
        length = 0
        longest_path = None
        for path in k_shortest_paths_res:
            if len(path) > length:
                longest_path = path

        if longest_path == None:
            logger.warn("longest path is none")
            return False
        used_node = list(set(used_node + longest_path)) # remove duplicated nodes by set

        while True: # length contains src and dst, thus minus 2
            # find an edge m with minimum residual bandwidth
            min_bandwidth = None
            current_node = longest_path[0]
            m_edge = None
            count = 0
            index = None
            for node in longest_path[1:]:
                if current_node == node:
                    logger.warn('duplicate nodes')
                    return False
                edge_bandwidth = substrate_network.get_link_bandwidth_free(current_node, node)
                if not min_bandwidth or edge_bandwidth < min_bandwidth:
                    min_bandwidth = edge_bandwidth
                    m_edge = [current_node, node]
                    index = count
                current_node = node
                count += 1

            if m_edge == None:
                logger.warn("m edge is None")
                return False
            # find the node with maximum residual CPU capacity
            # find m_head's adjacent edges
            m_head = m_edge[0]
            m_tail = m_edge[1]
            m_head_adjacent_edges = substrate_network.edges(m_head)
            m_tail_adjacent_edges = substrate_network.edges(m_tail)
            max_residual_cpu_capacity = 0
            candidate_node_head = None
            candidate_node_tail = None
            for e in m_head_adjacent_edges:
                adjacent_node = e[1]
                if adjacent_node in used_node:
                    continue
                residual_cpu_capacity = substrate_network.get_node_cpu_free(adjacent_node)
                if residual_cpu_capacity > max_residual_cpu_capacity:
                    max_residual_cpu_capacity = residual_cpu_capacity
                    candidate_node_head = adjacent_node
            if candidate_node_head != None:
                used_node.append(candidate_node_head)

            for e in m_tail_adjacent_edges:
                adjacent_node = e[1]
                if adjacent_node in used_node:
                    continue
                residual_cpu_capacity = substrate_network.get_node_cpu_free(adjacent_node)
                if residual_cpu_capacity > max_residual_cpu_capacity:
                    max_residual_cpu_capacity = residual_cpu_capacity
                    candidate_node_tail = adjacent_node
            if candidate_node_tail != None:
                used_node.append(candidate_node_tail)

            # compare two nodes and find the one with max residual
            candidate_node_n = None


            head_cpu = -1 if candidate_node_head == None else substrate_network.get_node_cpu_free(candidate_node_head)
            tail_cpu = -1 if candidate_node_tail == None else substrate_network.get_node_cpu_free(candidate_node_tail)
            candidate_node_n = candidate_node_head if head_cpu > tail_cpu else candidate_node_tail

            if candidate_node_n == None:
                logger.warn("candidate node is None")
                return False

            shortest_path_m_head_n = substrate_network.get_minimum_latency_path(m_head, candidate_node_n)
            shortest_path_n_m_tail = substrate_network.get_minimum_latency_path(candidate_node_n, m_tail)
            if shortest_path_n_m_tail == None or shortest_path_m_head_n == None:
                logger.warn('have not shortest path')
                return False


            longest_path = longest_path[:index] + shortest_path_m_head_n + shortest_path_n_m_tail[1:-1] + longest_path[index+1:]
            new_list = list(set(longest_path[:]))
            new_list.remove(src_substrate_node)
            new_list.remove(dst_substrate_node)
            if len(new_list) >= number_of_vnfs:
                break

        route_info = {}

        used_node = [src_substrate_node, dst_substrate_node]
        current_vnf = src_vnf

        for node in longest_path:
            if current_vnf.id in route_info:
                route_info[current_vnf.id].append(node)
            else:
                route_info[current_vnf.id] = [node]

            if sfc.get_next_vnf(current_vnf).id == 'dst':
                continue
            if node not in used_node:
                # current_vnf =
                cpu_request = sfc.get_vnf_cpu_request(sfc.get_next_vnf(current_vnf))
                cpu_available = substrate_network.get_node_cpu_free(node)
                if cpu_request > cpu_available:
                    # if node has not sufficient cpu, check next edge.
                    logger.warn("node %s has not sufficient cpu, available: %s", node, cpu_available)
                    continue
                current_vnf = sfc.get_next_vnf(current_vnf)
                if current_vnf.id in route_info:
                    route_info[current_vnf.id].append(node)
                else:
                    route_info[current_vnf.id] = [node]
                used_node.append(node)

        ## check if all vnfs have found a proper substrate network node.
        # if all vnf have found a substrate node,
        # length of route info is equal to the number of vnfs plus 1,
        # which the one is src.
        # dst is NOT yet included in route info.
        if len(route_info) < number_of_vnfs + 1:
            logger.warn('some nodes are not deployed')
            return False
        else:
            route_info[dst_vnf.id] = [] # placeholder, add dst to route info
            latency = 0
            current_vnf = src_vnf
            bandwidth_usage_info = {}

            while current_vnf.id != dst_vnf.id:
                path = route_info[current_vnf.id]
                next_vnf = sfc.get_next_vnf(current_vnf)

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
                        logger.warn('Bandwidth resources is not sufficient')
                        return False
                    bandwidth_usage_info[edge_key] = residual_bandwidth
                    latency = latency + substrate_network.get_link_latency(path[i], path[i + 1])
                current_vnf = next_vnf

            self.route_info = route_info
            self.latency = latency
            return True















       