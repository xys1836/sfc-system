import sched, time
from threading import Timer
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
# ch = logging.StreamHandler()
ch = logging.FileHandler('./logs/substrate_network_controller.log')
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

class SubstrateNetworkController():
    pass
    def __init__(self, nw):
        pass
        self.substrate_network = nw
        self.node_info = {}
        self.alg = None
        self.sfc_list = []
        self.isStopped = True
        self.update_interval = 1
        self.cpu_threshold = 0.8
        self.over_threshold_nodes_list = []

    def start(self):
        if not self.isStopped:
            self.isStopped = True
            time.sleep(2*self.update_interval)
        self.isStopped = False
        self.update()

    def output_nodes_information(self):
        self.substrate_network.print_out_nodes_information()

    def output_edges_information(self):
        self.substrate_network.print_out_edges_information()

    def get_nodes_information(self):
        for node in self.substrate_network.nodes():
            self.node_info[node] = self.get_node_information(node)

    def get_node_information(self, node_id):
        cpu_used = self.substrate_network.get_node_cpu_used(node_id)
        cpu_free = self.substrate_network.get_node_cpu_free(node_id)
        cpu_capacity = self.substrate_network.get_node_cpu_capacity(node_id)
        sfc_vnf_list = self.substrate_network.get_node_sfc_vnf_list(node_id)
        return (cpu_used, cpu_free, cpu_capacity, sfc_vnf_list)

    def update(self):
        self.substrate_network.update()
        self.check_cpu_threshold()
        logger.warn(self.over_threshold_nodes_list)
        logger.warn(self.sfc_list)
        if not self.isStopped:
            Timer(self.update_interval, self.update, ()).start()

    def check_node_cpu_threshold(self, node_id):
        cpu_used = self.substrate_network.get_node_cpu_used(node_id)
        cpu_capacity = self.substrate_network.get_node_cpu_capacity(node_id)
        if float(cpu_used)/float(cpu_capacity) > self.cpu_threshold:
            self.over_threshold_nodes_list.append(node_id)
            # print "node:", node_id, "over threshold"
            logger.warn("Node: %s, over threshold", str(node_id))

    def check_cpu_threshold(self):
        self.over_threshold_nodes_list = []
        for node in self.substrate_network.nodes():
            self.check_node_cpu_threshold(node)


    def stop(self):
        self.isStopped = True

    def deploy_sfc(self, sfc, alg):
        if sfc.id in self.sfc_list:
            print "sfc has been deployed"
            return
        alg.install_substrate_network(self.substrate_network)
        alg.install_SFC(sfc)
        alg.start_algorithm()
        route_info = alg.get_route_info()
        self.substrate_network.deploy_sfc(sfc, route_info)
        self.sfc_list.append(sfc.id)

    def get_route_info(self):
        return self.substrate_network.sfc_route_info

    def undeploy_sfc(self, sfc_id):
        self.stop()
        time.sleep(self.update_interval*2)
        self.substrate_network.undeploy_sfc(sfc_id)
        self.sfc_list.remove(sfc_id)
        # self.update()
        self.start()

    def handle_cpu_over_threshold(self):
        import copy
        sn = copy.deepcopy(self.substrate_network)
