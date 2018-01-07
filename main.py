
from controllers.substrate_network_controller import SubstrateNetworkController
from generate_substrate_network import substrate_network
# from generate_sfc import sfc
# from generate_sfc import sfc_dict
from algorithms.alg3 import ALG3
import numpy as np


from core.poisson_emitter import PoissonEmitter
from controllers.sfc_queue import SFCQueue
from controllers.sfc_generator import SFCGenerator
from controllers.sfc_controller import SFCController


import random

number_of_substrate_node = substrate_network.number_of_nodes()

sfc_dict = {
    "name": "sfc_1",
    "type": "xx",
    "vnf_list": [
        {"type": 2, "name": "vnf1", "CPU": random.randint(0, 50)},
        {"type": 2, "name": "vnf2", "CPU": random.randint(0, 50)},
        {"type": 2, "name": "vnf3", "CPU": random.randint(0, 50)},
        {"type": 2, "name": "vnf4", "CPU": random.randint(0, 50)},

    ],
    "bandwidth": random.randint(0, 50),
    "src_node": 1,
    "dst_node": 9,
    "latency": 10,
    "duration": 20
}


count = 0
sfc_queue = SFCQueue()
sfc_poisson_emitter = PoissonEmitter(10)
def generate_sfc(p):
    global count
    count = count + 1
    sfc_dict["name"] = "sfc_" + str(count)

    vnf_list = []
    number_of_vnfs = random.randint(2, 6)
    for i in range(0, number_of_vnfs):
        vnf_list.append({"type": 2, "name": "vnf" + str(i), "CPU": random.randint(1, 50)})
    bandwidth = random.randint(1, 50)
    src_node = random.randint(0, number_of_substrate_node -1 )
    dst_node = random.randint(0, number_of_substrate_node -1 )
    while(dst_node == src_node):
        dst_node = random.randint(0, number_of_substrate_node - 1)
    # lifetime = np.random.poisson(500)
    lifetime = int(round(np.random.exponential(500)))
    duration = lifetime
    sfc_dict["vnf_list"] = vnf_list
    sfc_dict["bandwidth"] = bandwidth
    sfc_dict["src_node"] = src_node
    sfc_dict["dst_node"] = dst_node
    sfc_dict["duration"] = duration

    # for test
    # vnf_list = []
    # number_of_vnfs = 6# random.randint(2, 6)
    # for i in range(0, number_of_vnfs):
    #     vnf_list.append({"type": 2, "name": "vnf" + str(i), "CPU": random.randint(1, 50)})
    # bandwidth = random.randint(1, 50)
    # src_node = random.randint(0, number_of_substrate_node - 1)
    # dst_node = random.randint(0, number_of_substrate_node - 1)
    # duration = random.randint(1000000, 2000000)
    # sfc_dict["vnf_list"] = vnf_list
    # sfc_dict["bandwidth"] = bandwidth
    # sfc_dict["src_node"] = src_node
    # sfc_dict["dst_node"] = dst_node
    # sfc_dict["duration"] = duration



    # print "***********"
    print count
    print sfc_dict
    # print "###########"


    sfc = SFCGenerator(sfc_dict).generate()
    sfc_queue.put_sfc(sfc)
    print "queue_size: " + str(sfc_queue.qsize())
    if count >= 1000:
        print "stop"
        sfc_poisson_emitter.stop()


sfc_poisson_emitter.start(generate_sfc, (None))

alg = ALG3()
sbn_controller = SubstrateNetworkController(substrate_network)
sbn_controller.sfc_queue = sfc_queue
sbn_controller.start()

while 1:
    pass
# isStop = False
# while(not isStop):
#     cmd = raw_input(">")
#     if cmd == "quit" or cmd == "exit":
#         print "is stop"
#         isStop = True
#         sbn_controller.stop()
#         sfc_poisson_emitter.stop()
#     # elif cmd == 'change cpu request':
#     #     sfc.change_node_cpu_request_to(3, 85)
#     elif cmd == 'update':
#         substrate_network.update_nodes_state()
#         substrate_network.update_bandwidth_state()
#     # elif cmd == "change bw request":
#     #     sfc.change_link_bandwidth_request_to(1, 100)
#     #     print sfc.get_link_bandwidth_request(vnf1.id, vnf2.id)
#     elif cmd == "mo":
#         sbn_controller.output_nodes_information()
#         sbn_controller.output_edges_information()
#     # elif cmd == "deploy":
#     #     sbn_controller.deploy_sfc(sfc, alg)
#     # elif cmd == "deploy2":
#     #     sbn_controller.deploy_sfc(sfc2, alg)
#     elif cmd == "get route info":
#         print sbn_controller.get_route_info()
#     elif cmd == "start":
#         sbn_controller.start()
#     elif cmd == "stop":
#         sbn_controller.stop()
#     # elif cmd == "undeploy":
#     #     sbn_controller.undeploy_sfc('sfc_1')
#     # elif cmd == "undeploy2":
#     #     sbn_controller.undeploy_sfc('sfc_2')
#     # elif cmd == "undeploy3":
#     #     sbn_controller.undeploy_sfc('sfc_3')
#     elif cmd == "handle":
#         alg1 = ALG3()
#         sbn_controller.handle_cpu_over_threshold(alg1)
#     # elif cmd == "set src":
#     #     sfc.set_input_throughput(20)
#     # elif cmd == "deploy3":
#     #     sbn_controller.deploy_sfc(sfc3, alg)
#     else:
#         print "no such cmd"
#     print cmd
