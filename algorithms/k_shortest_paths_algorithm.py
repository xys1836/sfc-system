import copy
import random
from utils.k_shortest_paths import k_shortest_paths
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
ch = logging.FileHandler('./logs/KShortestAlgorithm.log')
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





class KShortestPathsAlgorithm():
    def __init__(self):
        self.name = "k shortest paths algorithm"
        self.substrate_network = None
        self.sfc = None
        self.node_info = None
        self.route_info = None
        self.latency = None


    def clear_all(self):
        print "k shortest algorithm: clear all"
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
        self.algorithm(substrate_network, sfc)
        return

    def get_latency(self):
        return self.latency
    
    def get_route_info(self):
        return self.route_info

    def algorithm(self, substrate_network, sfc):
    
        print "k shortest algorithm: "

        nodes = substrate_network.nodes()
        ## Get src and dst vnf
        src_vnf = sfc.get_src_vnf()
        dst_vnf = sfc.get_dst_vnf()

        ## Get substrate network nodes that src and dst are assigned in advanced
        src_substrate_node = sfc.get_substrate_node(src_vnf)
        dst_substrate_node = sfc.get_substrate_node(dst_vnf)

        route_info = {}
        number_of_vnfs = sfc.get_number_of_vnfs()
        current_vnf = src_vnf
        current_substrate_node = src_substrate_node

        used_node = [src_substrate_node, dst_substrate_node]
        k = 1
        k_shortest_paths_res = k_shortest_paths(substrate_network, src_substrate_node, dst_substrate_node, k, 'latency')

        # find the longest single path ip:
        length = 0
        longest_path = None
        for path in k_shortest_paths_res:
            if len(path) > length:
                longest_path = path

        print "original longest path", longest_path
        if longest_path == None:
            print "longest path is none"
            return False
        used_node = list(set(used_node + longest_path)) # remove duplicated nodes by set

        # if len(longest_path) - 2 < number_of_vnfs:
        while True: # length contains src and dst, thus minus 2
            # find an edge m with minimum residual bandwidth
            min_bandwidth = None
            current_node = longest_path[0]
            m_edge = None
            count = 0
            index = None
            for node in longest_path[1:]:
                if current_node == node:
                    print 'duplicate nodes'
                    return False
                edge_bandwidth = substrate_network.get_link_bandwidth_free(current_node, node)
                if not min_bandwidth or edge_bandwidth < min_bandwidth:
                    min_bandwidth = edge_bandwidth
                    m_edge = [current_node, node]
                    index = count
                current_node = node
                count += 1

            if m_edge == None:
                print "m edge is None"
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
                print "candidate node is None"
                return False

            shortest_path_m_head_n = substrate_network.get_minimum_latency_path(m_head, candidate_node_n)
            shortest_path_n_m_tail = substrate_network.get_minimum_latency_path(candidate_node_n, m_tail)
            if shortest_path_n_m_tail == None or shortest_path_m_head_n == None:
                print 'have not shortest path'
                return False


            longest_path = longest_path[:index] + shortest_path_m_head_n + shortest_path_n_m_tail[1:-1] + longest_path[index+1:]
            print "longest path", longest_path
            new_list = list(set(longest_path[:]))
            new_list.remove(src_substrate_node)
            new_list.remove(dst_substrate_node)
            print "new list", new_list
            if len(new_list) >= number_of_vnfs:
                break

        print 'after while'
        print longest_path


        route_info = {}

        used_node = [src_substrate_node, dst_substrate_node]
        current_vnf = src_vnf

        count = 0
        index = 0
        for node in longest_path:
            print route_info
            if node in used_node:
                if current_vnf.id in route_info:
                    route_info[current_vnf.id].append(node)
                else:
                    route_info[current_vnf.id] = [node]
            else:
                route_info[current_vnf.id].append(node)
                next_vnf = sfc.get_next_vnf(current_vnf)

                # cpu_request = sfc.get_vnf_cpu_request(next_vnf)
                # cpu_available = substrate_network.get_node_cpu_free(node)
                #
                # if cpu_request > cpu_available:
                #     # if node has not sufficient cpu, check next edge.
                #     logger.debug("node %s has not sufficient cpu", node)
                #     print "node %s has not sufficient cpu", node, cpu_available
                #     route_info[current_vnf.id].append(node)
                #     continue
                route_info[next_vnf.id] = [node]
                current_vnf = next_vnf






            # count += 1
            # if node in used_node:
            #     print 'node has been used ', node
            #     continue
            # next_vnf = sfc.get_next_vnf(current_vnf)  # vnf 1
            # if next_vnf == None:
            #     # number of nodes is more than number of vnfs
            #     # indicate success
            #     print 'next vnf is None'
            #     break
            #
            # # check cpu
            # cpu_request = sfc.get_vnf_cpu_request(next_vnf)
            # cpu_available = substrate_network.get_node_cpu_free(node)
            # if cpu_request > cpu_available:
            #     # if node has not sufficient cpu, check next edge.
            #     logger.debug("node %s has not sufficient cpu", node)
            #     print "node %s has not sufficient cpu", node, cpu_available
            #     continue
            #
            # route_info[current_vnf.id] = longest_path[index:count]
            # current_vnf = next_vnf
            # index = count - 1

        latency = 0
        print route_info
        if current_vnf == None or current_vnf.id == 'dst':
            # indicate success
            route_info[sfc.get_previous_vnf(dst_vnf).id] += longest_path[count-1:]
            route_info[dst_vnf.id] = []

            current_vnf = src_vnf
            bandwidth_usage_info = {}
            print route_info
            while current_vnf.id != 'dst':
                path = route_info[current_vnf.id]
                print path
                next_vnf = sfc.get_next_vnf(current_vnf)

                bandwidth_request = sfc.get_link_bandwidth_request(current_vnf.id, next_vnf.id)

                length = len(path)
                for i in range(0, length - 1):
                    edge_key = frozenset((path[i], path[i + 1]))
                    print edge_key
                    residual_bandwidth = None
                    if edge_key in bandwidth_usage_info:
                        residual_bandwidth = bandwidth_usage_info[edge_key] - bandwidth_request
                    else:
                        residual_bandwidth = substrate_network.get_link_bandwidth_free(path[i],
                                                                                       path[i + 1]) - bandwidth_request
                    if residual_bandwidth < 0:
                        logger.warning('Bandwidth resources is not sufficient')
                        print 'bandwidth resource is not sufficinet'
                        return False
                    bandwidth_usage_info[edge_key] = residual_bandwidth
                    latency = latency + substrate_network.get_link_latency(path[i], path[i + 1])
                current_vnf = next_vnf



        else:
            print " some node has not been deployed 2"
            print current_vnf.id
            return False


        print route_info
        print latency














       