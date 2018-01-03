import sched, time
from threading import Timer
import logging
from algorithms.alg3 import ALG3
import copy

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
    def __init__(self, nw):
        pass
        self.substrate_network = nw
        self.node_info = {}
        self.sfc_list = []
        self.is_stopped = True
        self.update_interval = 1
        self.cpu_threshold = 0.8
        self.over_threshold_nodes_list = []
        self.timer = None
        self.sfc_queue = None
        self.sfc_id_duration = {}

    def start(self):
        if not self.is_stopped:
            self.is_stopped = True
            time.sleep(2*self.update_interval)
        self.is_stopped = False
        self.update()
        import thread
        thread.start_new_thread(self.run, ())

    def output_nodes_information(self):
        self.substrate_network.print_out_nodes_information()

    def output_edges_information(self):
        self.substrate_network.print_out_edges_information()

    def output_info(self):
        self.output_nodes_information()
        self.output_edges_information()

    def get_nodes_information(self):
        for node in self.substrate_network.nodes():
            self.node_info[node] = self.get_node_information(node)

    def get_node_information(self, node_id):
        cpu_used = self.substrate_network.get_node_cpu_used(node_id)
        cpu_free = self.substrate_network.get_node_cpu_free(node_id)
        cpu_capacity = self.substrate_network.get_node_cpu_capacity(node_id)
        sfc_vnf_list = self.substrate_network.get_node_sfc_vnf_list(node_id)
        total_cpu_used = self.substrate_network.total_cpu_used
        total_cpu_capacity = self.substrate_network.total_cpu_capacity
        return (cpu_used, cpu_free, cpu_capacity, sfc_vnf_list, total_cpu_used, total_cpu_capacity)

    def update(self):

        self.substrate_network.update()
        self.check_cpu_threshold()
        logger.warn(self.over_threshold_nodes_list)
        logger.warn(self.sfc_list)
        self.check_sfc_duration()
        if not self.is_stopped:
            self.timer = Timer(self.update_interval, self.update, ()).start()

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

    def check_sfc_duration(self):
        remove_list = []
        for sfc_id, duration in self.sfc_id_duration.items():
            if duration <= 1:
                remove_list.append(sfc_id)
                continue
            self.sfc_id_duration[sfc_id] = duration - 1
        for sfc_id in remove_list:
            self.undeploy_sfc(sfc_id)



    def stop(self):
        self.is_stopped = True
        if self.timer:
            self.timer.cancel()

    def deploy_sfc(self, sfc):
        if sfc.id in self.sfc_list:
            print "sfc has been deployed"
            return
        alg = ALG3()
        alg.install_substrate_network(self.substrate_network)
        alg.install_SFC(sfc)
        alg.start_algorithm()
        route_info = alg.get_route_info()
        # print route_info
        if route_info:
            self.substrate_network.deploy_sfc(sfc, route_info)
            self.sfc_list.append(sfc.id)
            self.sfc_id_duration[sfc.id] = sfc.duration
            self.deploy_success()
        else:
            self.deploy_failed()
        print "__________________________________________"
        self.output_info()
        print ""


    def deploy_success(self):
        print "deploy succeed"

    def deploy_failed(self):
        print "deploy failed"

    def get_route_info(self):
        return self.substrate_network.sfc_route_info

    def undeploy_sfc(self, sfc_id):
        if sfc_id not in self.sfc_list:
            print sfc_id, "not on the substrate network"
            return
        # self.stop()
        # time.sleep(self.update_interval*2)
        self.substrate_network.undeploy_sfc(sfc_id)
        self.sfc_list.remove(sfc_id)
        del self.sfc_id_duration[sfc_id]
        # self.update()
        # self.start()

    def handle_cpu_over_threshold(self, alg):
        import copy
        ## undeploy the sfc, redeploy sfc by disable the over threshold cpu
        self.stop()
        for node in self.over_threshold_nodes_list:
            # (sfc_id, vnf) = sn.get_node_sfc_vnf_list(node)
            sfc_vnf_list = self.substrate_network.get_node_sfc_vnf_list(node)
            for (sfc_id, vnf) in sfc_vnf_list:
                ## todo: here we should consider which sfc need to be undployed. May according to priority or some history data or SLA. or cost...
                sfc = self.substrate_network.get_sfc_by_id(sfc_id)
                self.undeploy_sfc(sfc_id)
                sn = copy.deepcopy(self.substrate_network)
                sn.set_node_cpu_capacity(node, 0)
                sn.set_node_cpu_free(node, 0)
                alg.install_substrate_network(sn)
                alg.install_SFC(sfc)
                alg.start_algorithm()
                route_info = alg.get_route_info()
                if sfc.id in self.sfc_list:
                    print "sfc has been deployed"
                    return
                self.substrate_network.deploy_sfc(sfc, route_info)
                self.sfc_list.append(sfc.id)
                self.substrate_network.update()
        self.start()
        print ""


    def run(self):
        while not self.is_stopped:
            sfc = self.sfc_queue.peek_sfc()# this is blocking
            # print "Substrate network gets a new sfc", sfc.id
            self.deploy_sfc(sfc)

