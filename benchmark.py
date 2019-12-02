import time
from topology.simple_substrate_network import simple_six_node_topology
from generate_substrate_network import substrate_random_network

from sfc_examples import sfc1
from controllers.sfc_generator import SFCGenerator

from algorithms.alg3 import ALG3
from algorithms.random_algorithm import RandomAlgorithm
from algorithms.greedy_algorithm import GreedyAlgorithm
from algorithms.dynamic_programming_algorithm import DynamicProgrammingAlgorithm

ALG3 = ALG3()
ALG = DynamicProgrammingAlgorithm()
RandomAlgorithm = RandomAlgorithm()
GreedyAlgorithm = GreedyAlgorithm()

substrate_network = simple_six_node_topology
substrate_network = substrate_random_network

sfc_dict = sfc1.sfc
sfc = SFCGenerator(sfc_dict).generate()


def deploy_sfc(deployment_algorithm, substrate_network, sfc):
    print "---------- " + deployment_algorithm.name + " ----------------------------"
    start_time = time.time()
    deployment_algorithm.clear_all()
    deployment_algorithm.install_substrate_network(substrate_network)
    end_time = time.time()
    deployment_algorithm.install_SFC(sfc)

    print end_time - start_time
    start_time = time.time()
    deployment_algorithm.start_algorithm()
    end_time = time.time()

    route_info = deployment_algorithm.get_route_info()
    latency = deployment_algorithm.get_latency()
    return (route_info, latency, (end_time - start_time))



(route_info, latency, execution_time) = deploy_sfc(GreedyAlgorithm, substrate_network, sfc)
if route_info:
    print "success"
    print "route info: ", route_info
    print "latency: ", latency
    print "execution time: ", execution_time
    substrate_network.deploy_sfc(sfc, route_info)
    substrate_network.update_network_state()
else:
    print "failed"


(route_info, latency, execution_time) = deploy_sfc(ALG, substrate_network, sfc)
if route_info:
    print "success"
    print "route info: ", route_info
    print "latency: ", latency
    print "execution time: ", execution_time
    substrate_network.deploy_sfc(sfc, route_info)
    substrate_network.update_network_state()
else:
    print "failed"