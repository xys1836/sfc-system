import time
from topology.simple_substrate_network import simple_six_node_topology
# from generate_substrate_network import substrate_random_network
from generate_substrate_network import generate_random_network

from sfc_examples import sfc1
from controllers.sfc_generator import SFCGenerator

from algorithms.alg3 import ALG3
from algorithms.random_algorithm import RandomAlgorithm
from algorithms.greedy_algorithm import GreedyAlgorithm
from algorithms.dynamic_programming_algorithm import DynamicProgrammingAlgorithm
from algorithms.k_shortest_paths_algorithm import KShortestPathsAlgorithm
from algorithms.betweenness_centrality_algorithm import BetweennessCentralityAlgorithm

ALG3 = ALG3()
DPA = DynamicProgrammingAlgorithm()
RandomAlgorithm = RandomAlgorithm()
GreedyAlgorithm = GreedyAlgorithm()
KShortestPathsAlgorithm = KShortestPathsAlgorithm()
BetweennessCentralityAlgorithm = BetweennessCentralityAlgorithm()

substrate_network = simple_six_node_topology
# substrate_network = substrate_random_network
substrate_network = generate_random_network(100, 0.05)

sfc_dict = sfc1.sfc
sfc = SFCGenerator(sfc_dict).generate()


def deploy_sfc(deployment_algorithm, substrate_network, sfc):
    # print "---------- " + deployment_algorithm.name + " ----------------------------"
    deployment_algorithm.clear_all()
    deployment_algorithm.install_substrate_network(substrate_network)
    deployment_algorithm.install_SFC(sfc)
    start_time = time.time()
    deployment_algorithm.start_algorithm()
    end_time = time.time()
    route_info = deployment_algorithm.get_route_info()
    latency = deployment_algorithm.get_latency()
    return (route_info, latency, (end_time - start_time))

(route_info, latency, execution_time) = deploy_sfc(BetweennessCentralityAlgorithm, substrate_network, sfc)
if route_info:
    print "success"
    print "route info: ", route_info
    print "latency: ", latency
    print "execution time: ", execution_time
    substrate_network.deploy_sfc(sfc, route_info)
    substrate_network.update_network_state()
else:
    print "failed"

exit(0)
for i in range(0,10000):
    print '************************************************************************************************************'
    from generate_substrate_network import generate_random_network
    substrate_network = generate_random_network(100, 0.1)
    (route_info, latency, execution_time) = deploy_sfc(KShortestPathsAlgorithm, substrate_network, sfc)
    print 'KShortestPathsAlgorithm latency: ', latency
    print 'KShortestPathsAlgorithm execution time: ', execution_time

    (route_info, latency, execution_time) = deploy_sfc(GreedyAlgorithm, substrate_network, sfc)
    print 'GreedyAlgorithm latency: ', latency
    print 'GreedyAlgorithm execution time: ', execution_time
    (route_info, latency, execution_time) = deploy_sfc(RandomAlgorithm, substrate_network, sfc)
    print 'RandomAlgorithm latency: ', latency
    print 'RandomAlgorithm execution time: ', execution_time
    (route_info, latency, execution_time) = deploy_sfc(DPA, substrate_network, sfc)
    print 'DPA latency: ', latency
    print 'DPA execution time: ', execution_time
    print i
(route_info, latency, execution_time) = deploy_sfc(DPA, substrate_network, sfc)
if route_info:
    print "success"
    print "route info: ", route_info
    print "latency: ", latency
    print "execution time: ", execution_time
    substrate_network.deploy_sfc(sfc, route_info)
    substrate_network.update_network_state()
else:
    print "failed"