import time
import random
import copy
import sys
from topology.nsfnet import NSFNET
from topology.jpn48_network import JPN48
import matplotlib.pyplot as plt

from sfc_examples import sfc1
from controllers.sfc_generator import SFCGenerator

from algorithms.alg3 import ALG3
from algorithms.random_algorithm import RandomAlgorithm
from algorithms.greedy_algorithm import GreedyAlgorithm
from algorithms.dynamic_programming_algorithm import DynamicProgrammingAlgorithm
from algorithms.k_shortest_paths_algorithm import KShortestPathsAlgorithm
from algorithms.betweenness_centrality_algorithm import BetweennessCentralityAlgorithm

NUMBER_OF_EXPERIMENTS = 100
NUMBER_OF_EXPERIMENTS_FOR_RANDOM = 100
IS_UPDATE = False

DPAlgorithm = DynamicProgrammingAlgorithm()
GDAlgorithm = GreedyAlgorithm()
KPathsAlgorithm_1 = KShortestPathsAlgorithm(1)
KPathsAlgorithm_10 = KShortestPathsAlgorithm(10)
BCAlgorithm = BetweennessCentralityAlgorithm()
RAAlgorithm = RandomAlgorithm()

substrate_network = NSFNET
substrate_network_dp = copy.deepcopy(substrate_network)
substrate_network_gd = copy.deepcopy(substrate_network)
substrate_network_k1 = copy.deepcopy(substrate_network)
substrate_network_k10 = copy.deepcopy(substrate_network)
substrate_network_bc = copy.deepcopy(substrate_network)
substrate_network_ra = copy.deepcopy(substrate_network)


# sfc_dict = {
#     "name": "sfc_1",
#     "type": "xx",
#     "vnf_list": [
#         # {"type": 2, "name": "vnf1", "CPU": 10},
#         # {"type": 2, "name": "vnf2", "CPU": 20},
#         # {"type": 2, "name": "vnf3", "CPU": 30},
#         # {"type": 2, "name": "vnf4", "CPU": 40},
#         # {"type": 2, "name": "vnf5", "CPU": 40},
#         # {"type": 2, "name": "vnf6", "CPU": 40},
#
#     ],
#     "bandwidth": 10,
#     "src_node": 0,
#     "dst_node": 0,
#     "latency": 10,
#     "duration": 20
# }
#


dp_latency_list = []
gd_latency_list = []
ks1_latency_list = []
ks10_latency_list = []
bc_latency_list = []
ra_latency_list = []




def deploy_sfc(deployment_algorithm, substrate_network, sfc, update=False):
    # print "---------- " + deployment_algorithm.name + " ----------------------------"
    deployment_algorithm.clear_all()
    deployment_algorithm.install_substrate_network(substrate_network)
    deployment_algorithm.install_SFC(sfc)
    start_time = time.time()
    deployment_algorithm.start_algorithm()
    end_time = time.time()
    route_info = deployment_algorithm.get_route_info()
    latency = deployment_algorithm.get_latency()
    if update:
        substrate_network.deploy_sfc(sfc, route_info)
        substrate_network.update()
        substrate_network.print_out_edges_information()
        substrate_network.print_out_nodes_information()
    return (route_info, latency, (end_time - start_time))



def construct_sfc(src, dst, number_of_vnfs):
    sfc_dict = {
        "name": "sfc_1",
        "type": "xx",
        "vnf_list": [
            # {"type": 2, "name": "vnf1", "CPU": 10},
            # {"type": 2, "name": "vnf2", "CPU": 20},
            # {"type": 2, "name": "vnf3", "CPU": 30},
            # {"type": 2, "name": "vnf4", "CPU": 40},
            # {"type": 2, "name": "vnf5", "CPU": 40},
            # {"type": 2, "name": "vnf6", "CPU": 40},

        ],
        "bandwidth": 10,
        "src_node": 0,
        "dst_node": 0,
        "latency": 10,
        "duration": 20
    }

    sfc_dict['src_node'] = src
    sfc_dict['dst_node'] = dst
    for i in range(0, number_of_vnfs):
        name = 'vnf' + str(i + 1)
        vnf = {"type": 2, "name": name, "CPU": 10}
        sfc_dict['vnf_list'].append(vnf)
    sfc = SFCGenerator(sfc_dict).generate()
    return sfc

def one_short_experiment(sfc):
    (dp_route_info, dp_latency, dp_execution_time) = deploy_sfc(DPAlgorithm, substrate_network_dp, sfc, update=IS_UPDATE)
    (gd_route_info, gd_latency, gd_execution_time) = deploy_sfc(GDAlgorithm, substrate_network_gd, sfc, update=IS_UPDATE)
    (ks1_route_info, ks1_latency, ks1_execution_time) = deploy_sfc(KPathsAlgorithm_1, substrate_network_k1,
                                                                       sfc, update=IS_UPDATE)
    (ks10_route_info, ks10_latency, ks10_execution_time) = deploy_sfc(KPathsAlgorithm_10, substrate_network_k10,
                                                                          sfc, update=IS_UPDATE)
    (bc_route_info, bc_latency, bc_execution_time) = deploy_sfc(BCAlgorithm, substrate_network_bc,
                                                                    sfc, update=IS_UPDATE)
    sum_latency = []
    for i in range(0, NUMBER_OF_EXPERIMENTS_FOR_RANDOM):
        (ra_route_info, ra_latency, ra_execution_time) = deploy_sfc(RAAlgorithm, substrate_network, sfc, update=IS_UPDATE)
        if ra_latency != None:
            sum_latency.append(ra_latency)
    ra_latency = sum(sum_latency) * 1.0 / len(sum_latency)

    return (dp_latency, gd_latency, ks1_latency, ks10_latency, bc_latency, ra_latency)


def output_results_csv(res, file_name):
    with open(file_name, "a") as f:
        line = str(res)[1:-1] + "\n"
        f.write(line)


def experiment(number_of_experiment, number_of_vnfs):
    count = 0
    while count < number_of_experiment:
        node_list = list(substrate_network.nodes())
        random.shuffle(node_list)
        src = node_list[0]
        dst = node_list[1]
        sfc = construct_sfc(src, dst, number_of_vnfs=number_of_vnfs)
        res = one_short_experiment(sfc)
        if None in res:
            print 'NONE'
            continue
        else:
            count += 1
            print count
            output_results_csv(res, './results/NSFNET/exp-' + str(number_of_vnfs) +'.csv')

for number_of_vnfs  in [2,3,4,5]:
    experiment(NUMBER_OF_EXPERIMENTS, number_of_vnfs=number_of_vnfs)
