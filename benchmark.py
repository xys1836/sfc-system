import time
from topology.simple_substrate_network import simple_six_node_topology
from sfc_examples import sfc1
from controllers.sfc_generator import SFCGenerator

from algorithms.alg3 import ALG3
from algorithms.random_algorithm import RandomAlgorithm
from algorithms.greedy_algorithm import GreedyAlgorithm
from algorithms.dynamic_programming_algorithm import DynamicProgrammingAlgorithm

ALG = DynamicProgrammingAlgorithm()
ALG = RandomAlgorithm()
# ALG = GreedyAlgorithm()

substrate_network = simple_six_node_topology

sfc_dict = sfc1.sfc
sfc = SFCGenerator(sfc_dict).generate()

alg = ALG
alg.clear_all()
alg.install_substrate_network(substrate_network)
alg.install_SFC(sfc)
s = time.time()
if alg.start_algorithm():
    print "success"
else:
    print "failed"
s2 = time.time()

route_info = alg.get_route_info()
latency = alg.get_latency()
print route_info
print latency

        # |-> For test dy algorithm
        # alg2 = ALG3()
        # alg2.clear_all()
        # alg2.install_substrate_network(self.substrate_network)
        # alg2.install_SFC(sfc)
        # alg2.start_algorithm()
        # route_info_2 = alg2.get_route_info()
        # latency_2 = alg2.get_latency()
        # For test dy algorithm END ->|

