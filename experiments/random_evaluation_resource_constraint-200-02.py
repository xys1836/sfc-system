import time
import random
import copy

from controllers.sfc_generator import SFCGenerator
from generate_substrate_network import generate_random_network
from algorithms.random_algorithm import RandomAlgorithm
from algorithms.greedy_algorithm import GreedyAlgorithm
from algorithms.dynamic_programming_algorithm import DynamicProgrammingAlgorithm
from algorithms.k_shortest_paths_algorithm import KShortestPathsAlgorithm
from algorithms.betweenness_centrality_algorithm import BetweennessCentralityAlgorithm

IS_UPDATE = True

DPAlgorithm = DynamicProgrammingAlgorithm()
GDAlgorithm = GreedyAlgorithm()
KPathsAlgorithm_1 = KShortestPathsAlgorithm(1)
KPathsAlgorithm_10 = KShortestPathsAlgorithm(10)
BCAlgorithm = BetweennessCentralityAlgorithm()
RAAlgorithm = RandomAlgorithm()

substrate_network = generate_random_network(200, 0.2)

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
    try:
        start_time = time.time()
        deployment_algorithm.start_algorithm()
        end_time = time.time()
        route_info = deployment_algorithm.get_route_info()
        latency = deployment_algorithm.get_latency()
    except:
        route_info, latency = None, None
        end_time, start_time = 0, 0
    if update:
        substrate_network.deploy_sfc(sfc, route_info)
        substrate_network.update()
    return (route_info, latency, (end_time - start_time))



def construct_sfc(src, dst, number_of_vnfs):
    sfc_dict = {
        "name": "sfc_1",
        "type": "xx",
        "vnf_list": [

        ],
        "bandwidth": random.randint(5, 10),
        "src_node": 0,
        "dst_node": 0,
        "latency": 10,
        "duration": 20
    }

    sfc_dict['src_node'] = src
    sfc_dict['dst_node'] = dst
    for i in range(0, number_of_vnfs):
        name = 'vnf' + str(i + 1)
        vnf = {"type": 2, "name": name, "CPU": random.randint(5, 10)}
        sfc_dict['vnf_list'].append(vnf)
    # print sfc_dict
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
    (ra_route_info, ra_latency, ra_execution_time) = deploy_sfc(RAAlgorithm, substrate_network_ra, sfc, update=IS_UPDATE)

    return (dp_latency, gd_latency, ks1_latency, ks10_latency, bc_latency, ra_latency)


def output_results_csv(res, file_name):
    with open(file_name, "a") as f:
        line = str(res)[1:-1] + "\n"
        f.write(line)

def experiment(number_of_experiment, number_of_vnfs):
    count = 0
    failed_count = [0, 0, 0, 0, 0, 0]
    for i in range(0, number_of_experiment):
        node_list = list(substrate_network.nodes())
        random.shuffle(node_list)
        src = node_list[0]
        dst = node_list[1]
        sfc = construct_sfc(src, dst, number_of_vnfs=number_of_vnfs)
        latency_list = one_short_experiment(sfc)

        for i in range(0, len(latency_list)):
            if latency_list[i] == None:
                failed_count[i] += 1
    return failed_count

for ne in [100, 200, 300, 400, 500]:
    for nv in [2, 3, 4, 5]:
        for count in range(0, 10):
            substrate_network_dp = copy.deepcopy(substrate_network)
            substrate_network_gd = copy.deepcopy(substrate_network)
            substrate_network_k1 = copy.deepcopy(substrate_network)
            substrate_network_k10 = copy.deepcopy(substrate_network)
            substrate_network_bc = copy.deepcopy(substrate_network)
            substrate_network_ra = copy.deepcopy(substrate_network)
            failed_count = experiment(ne, number_of_vnfs=nv)

            cpu_rate = []
            bw_rate = []

            for substrate_nw in [substrate_network_dp, substrate_network_gd, substrate_network_k1, substrate_network_k10,
                         substrate_network_bc, substrate_network_ra]:
                cpu_rate.append(substrate_nw.get_cpu_utilization_rate())
                bw_rate.append(substrate_nw.get_bandwidth_utilization_rate())

            output_results_csv(str(failed_count), './results/random/200/02/resource_constraints/' + str(ne) + '-' + str(nv) + '-results-failed-count.csv')
            output_results_csv(str(cpu_rate), './results/random/200/02/resource_constraints/' + str(ne) + '-' + str(nv) + '-results-cpu-rate.csv')
            output_results_csv(str(bw_rate), './results/random/200/02/resource_constraints/' + str(ne) + '-' + str(nv) + '-results-bw-rate.csv')

print 'finish'