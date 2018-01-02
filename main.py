
from controllers.substrate_network_controller import SubstrateNetworkController
from generate_substrate_network import substrate_network
from generate_sfc import sfc
from algorithms.alg3 import ALG3
import copy

sfc2 = copy.deepcopy(sfc)

sfc2.id = "sfc_2"
sfc2.set_src_substrate_node(2)
sfc2.set_dst_substrate_node(8)

sfc3 = copy.deepcopy(sfc)
sfc3.id = "sfc_3"
sfc2.set_src_substrate_node(3)
sfc2.set_dst_substrate_node(7)

alg = ALG3()
sbn_controller = SubstrateNetworkController(substrate_network)
sbn_controller.start()


isStop = False
while(not isStop):
    cmd = raw_input(">")
    if cmd == "quit" or cmd == "exit":
        print "is stop"
        isStop = True
        sbn_controller.stop()
    # elif cmd == 'change cpu request':
    #     sfc.change_node_cpu_request_to(3, 85)
    elif cmd == 'update':
        substrate_network.update_nodes_state()
        substrate_network.update_bandwidth_state()
    # elif cmd == "change bw request":
    #     sfc.change_link_bandwidth_request_to(1, 100)
    #     print sfc.get_link_bandwidth_request(vnf1.id, vnf2.id)
    elif cmd == "mo":
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
        sbn_controller.undeploy_sfc('sfc_1')
    elif cmd == "undeploy2":
        sbn_controller.undeploy_sfc('sfc_2')
    elif cmd == "undeploy3":
        sbn_controller.undeploy_sfc('sfc_3')
    elif cmd == "handle":
        alg1 = ALG3()
        sbn_controller.handle_cpu_over_threshold(alg1)
    elif cmd == "set src":
        sfc.set_input_throughput(20)
    elif cmd == "deploy3":
        sbn_controller.deploy_sfc(sfc3, alg)
    else:
        print "no such cmd"
    print cmd
