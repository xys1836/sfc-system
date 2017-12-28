from core.sfc import SFC
from core.vnf import VNF
from generate_substrate_network import substrate_network

src_vnf = VNF('src')
src_vnf.set_cpu_request(0)
src_vnf.set_outcome_interface_bandwidth(20)
dst_vnf = VNF('dst')
dst_vnf.set_cpu_request(0)
sfc = SFC(src_vnf, dst_vnf)
vnf1 = VNF(1)
vnf1.set_cpu_request(10)
vnf1.set_outcome_interface_bandwidth(10)
vnf2 = VNF(2)
vnf2.set_cpu_request(20)
vnf2.set_outcome_interface_bandwidth(20)
vnf3 = VNF(3)
vnf3.set_cpu_request(30)
vnf3.set_outcome_interface_bandwidth(30)
sfc.id = 'sfc_1'
sfc.add_vnf(vnf1)
sfc.add_vnf(vnf2)
sfc.add_vnf(vnf3)
sfc.connect_two_vnfs(src_vnf, vnf1)
sfc.connect_two_vnfs(vnf1, vnf2)
sfc.connect_two_vnfs(vnf2, vnf3)
sfc.connect_two_vnfs(vnf3, dst_vnf)
sfc.set_latency_request(10)
sfc.set_src_substrate_node(0)
sfc.set_dst_substrate_node(7)

import copy
sfc2 = copy.deepcopy(sfc)
sfc2.id = "sfc_2"

from algorithms.alg3 import ALG3
alg = ALG3()

from core.monitor import Monitor
monitor = Monitor(substrate_network)
isStop = False

from controllers.substrate_network_controller import SubstrateNetworkController
sbn_controller = SubstrateNetworkController(substrate_network)


sbn_controller.start()

while(not isStop):
    cmd = raw_input(">")
    if cmd == "quit" or cmd == "exit":
        print "is stop"
        isStop = True
        sbn_controller.stop()
    elif cmd == 'change cpu request':
        sfc.change_node_cpu_request_to(3, 85)
    elif cmd == 'update':
        substrate_network.update_nodes_state()
        substrate_network.update_bandwidth_state()
    elif cmd == "change bw request":
        sfc.change_link_bandwidth_request_to(1, 100)
        print sfc.get_link_bandwidth_request(vnf1.id, vnf2.id)

    elif cmd == "bw info":
        substrate_network.print_out_edges_information()
    elif cmd == "mo":
        # sbn_controller.update()
        sbn_controller.output_nodes_information()
        sbn_controller.output_edges_information()
    elif cmd == "deploy":
        sbn_controller.deploy_sfc(sfc, alg)
    elif cmd == "deploy2":
        sbn_controller.deploy_sfc(sfc2, alg)
    elif cmd == "get route info":
        print sbn_controller.get_route_info()
    elif cmd == "start":
        sbn_controller.start()
    elif cmd == "stop":
        sbn_controller.stop()
    elif cmd == "undeploy":
        # substrate_network.undeploy_sfc("sfc_1")
        sbn_controller.undeploy_sfc('sfc_1')
    elif cmd == "handle":
        alg1 = ALG3()
        sbn_controller.handle_cpu_over_threshold(alg1)
    else:
        print "no such cmd"
    print cmd


def parseCmd(cmd):
    cmd = cmd.split(' ')
    if cmd[0] == "sb":
        if cmd[1] == "set":
            if cmd[2] == "node":
                print cmd
