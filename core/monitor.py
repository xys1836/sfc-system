import sys
import sched
import time
class Monitor():
    def __init__(self, nw):
        pass
        self.substrate_network = nw
        # self.scheduler = sched.scheduler(time.time, time.sleep)

    def start(self):

        pass


    def stop(self):
        pass
    def collect_information(self):
        pass

    def get_node_information(self):
        print "get node information"
        for node in self.substrate_network.nodes():
            print "node:",node, \
                self.substrate_network.get_node_cpu_free(node)

    def output_node_information(self):
        pass




