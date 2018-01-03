from core.sfc import SFC
from core.vnf import VNF
from vnfs.vnf_type_1 import VNFType1
import random
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



# from core.poisson_emitter import PoissonEmitter
# from controllers.sfc_queue import SFCQueue
# from controllers.sfc_generator import SFCGenerator
# from controllers.sfc_controller import SFCController
#
# count = 0
# sfc_queue = SFCQueue()
# def generate_sfc(sfc_dict):
#     global count
#     count = count + 1
#     sfc_dict["name"] = "sfc_" + str(count)
#     sfc = SFCGenerator(sfc_dict).generate()
#     sfc_queue.put_sfc(sfc)
#
# sfc_poisson_emitter = PoissonEmitter(5)
# sfc_poisson_emitter.start(generate_sfc, sfc_dict)
# # sfc_controller = SFCController()
# # sfc_controller.start(sfc_queue)
#
# # sfc = SFCGenerator(sfc_dict).generate()
# print ""