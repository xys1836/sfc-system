from networkx import networkx as nx
from basic_object import BasicObject
import math
class Net(nx.Graph):
    def __init__(self):
        nx.Graph.__init__(self)

    def _get_node_attribute(self, node_id, attr):
        return self.nodes[node_id][attr]
    def _set_node_attribute(self, node_id, **attr):
        self.add_node(node_id, **attr)
        return
    def reset_node_cpu_capacity(self, node_id, cpu_capacity):
        self.set_node_cpu_capacity(node_id, cpu_capacity)
        self.set_node_cpu_used(node_id, 0)
        self.set_node_cpu_free(node_id, cpu_capacity)
        return
    def init_node_cpu_capacity(self, node_id, cpu_capacity):
        self.reset_node_cpu_capacity(node_id, cpu_capacity)
        return
    def set_node_cpu_capacity(self, node_id, cpu_capacity):
        self._set_node_attribute(node_id, cpu_capacity=cpu_capacity)
        return cpu_capacity
    def set_node_cpu_used(self, node_id, cpu_used):
        return self._set_node_attribute(node_id, cpu_used = cpu_used)
    def set_node_cpu_free(self, node_id, cpu_free):
        return self._set_node_attribute(node_id, cpu_free = cpu_free)
    def get_node_cpu_capacity(self, node_id):
        return self._get_node_attribute(node_id, "cpu_capacity")
    def get_node_cpu_used(self, node_id):
        return self._get_node_attribute(node_id, "cpu_used")
    def get_node_cpu_free(self, node_id):
        return self._get_node_attribute(node_id, "cpu_free")
    def allocate_cpu_resource(self, node_id, cpu_amount):
        cpu_capacity = self.get_node_cpu_capacity(node_id)
        cpu_free = self.get_node_cpu_free(node_id)
        cpu_used = self.get_node_cpu_used(node_id)
        if cpu_amount > cpu_free:
            return False
        else:
            self.set_node_cpu_free(node_id, cpu_free-cpu_amount)
            self.set_node_cpu_used(node_id, cpu_used+cpu_amount)
            return True
        return False

    def _set_link_attribute(self, u, v, **attr):
        self.add_edge(u, v, **attr)
    def _get_link_attribute(self, u, v, attr):
        return self.edges[u, v][attr]
    def get_link_bandwidth_capacity(self, u, v):
        return self._get_link_attribute(u, v, 'bandwidth_capacity')
    def get_link_bandwidth_used(self, u, v):
        return self._get_link_attribute(u, v, 'bandwidth_used')
    def get_link_bandwidth_free(self, u, v):
        return self._get_link_attribute(u, v, 'bandwidth_free')
    def reset_bandwidth_capacity(self,u, v, bw_c):
        self.set_link_bandwidth_capacity(u, v, bw_c)
        self.set_link_bandwidth_used(u, v, 0)
        self.set_link_bandwidth_free(u, v, bw_c)
        return bw_c
    def init_bandwidth_capacity(self, u, v, bw_c):
        return self.reset_bandwidth_capacity(u, v, bw_c)
    def set_link_bandwidth_capacity(self, u, v, bw_c):
        self._set_link_attribute(u, v, bandwidth_capacity=bw_c)
        return bw_c
    def set_link_bandwidth_used(self, u, v, bw_u):
        self._set_link_attribute(u, v, bandwidth_used=bw_u)
        return bw_u
    def set_link_bandwidth_free(self, u, v, bw_f):
        self._set_link_attribute(u, v, bandwidth_free=bw_f)
        return bw_f
    def allocate_bandwidth_resource(self, u, v, bw_amount):
        bw_c = self.get_link_bandwidth_capacity(u, v)
        bw_u = self.get_link_bandwidth_used(u, v)
        bw_f = self.get_link_bandwidth_free(u,v)
        if bw_amount > bw_f:
            return False
        else:
            self.set_link_bandwidth_used(u, v, bw_u+bw_amount)
            self.set_link_bandwidth_free(u, v, bw_f-bw_amount)
            return True
        return False

    def allocate_bandwidth_resource_path(self, path, bw_amount):
        length = len(path)
        for i in range(0, length-1):
            print i
            self.allocate_bandwidth_resource(path[i], path[i+1], bw_amount)


    def get_link_latency(self, u, v):
        return self._get_link_attribute(u, v, 'latency')
    def set_link_latency(self, u, v, bw_l):
        self._set_link_attribute(u, v, latency=bw_l)
    def init_link_latency(self, u, v, bw_l):
        self.set_link_latency(u, v, bw_l)

    def get_neighbours(self, node_id):
        return self.neighbors(node_id)

    def all_shortest_paths(self):
        r = nx.all_pairs_dijkstra(self, weight='latency')
        print [n for n in r]
    def get_shortest_paths(self, src, dst, weight):
        try:
            return nx.shortest_path(self, src, dst, weight=weight)
        except:
            return None
    def get_minimum_latency_path(self, src, dst):
        return self.get_shortest_paths(src, dst, 'latency')
    def get_minimum_free_bandwidth(self, path):
        length = len(path)
        minimum_free_bandwidth = float('inf')
        for i in range(0, length-1):
            print i
            free_bandwidth = self.get_link_bandwidth_free(path[i], path[i+1])
            if free_bandwidth < minimum_free_bandwidth:
                minimum_free_bandwidth = free_bandwidth
        return minimum_free_bandwidth
    def get_single_source_minimum_latency_path(self, src):
        return nx.single_source_dijkstra(self, source=src, cutoff=None, weight='latency')




if __name__ == '__main__':
    substrate_network = Net()
    substrate_network.init_bandwidth_capacity(1, 6, 100)
    substrate_network.init_bandwidth_capacity(1, 2, 100)
    substrate_network.init_bandwidth_capacity(2, 3, 100)
    substrate_network.init_bandwidth_capacity(3, 4, 100)
    substrate_network.init_bandwidth_capacity(4, 5, 100)
    substrate_network.init_bandwidth_capacity(5, 6, 100)
    substrate_network.init_bandwidth_capacity(2, 6, 100)
    substrate_network.init_bandwidth_capacity(2, 5, 100)
    substrate_network.init_bandwidth_capacity(3, 5, 100)

    substrate_network.init_link_latency(1, 6, 2)
    substrate_network.init_link_latency(1, 2, 2)
    substrate_network.init_link_latency(2, 3, 2)
    substrate_network.init_link_latency(3, 4, 2)
    substrate_network.init_link_latency(4, 5, 2)
    substrate_network.init_link_latency(5, 6, 2)
    substrate_network.init_link_latency(2, 6, 2)
    substrate_network.init_link_latency(2, 5, 2)
    substrate_network.init_link_latency(3, 5, 2)

    substrate_network.init_node_cpu_capacity(1, 100)
    substrate_network.init_node_cpu_capacity(2, 100)
    substrate_network.init_node_cpu_capacity(3, 100)
    substrate_network.init_node_cpu_capacity(4, 100)
    substrate_network.init_node_cpu_capacity(5, 100)
    substrate_network.init_node_cpu_capacity(6, 100)

    print substrate_network.nodes().data()
    print substrate_network.edges().data()
    print substrate_network.get_link_latency(1, 2)
    print substrate_network.get_link_bandwidth_free(1, 2)
    print [n for n in substrate_network.get_neighbours(6)]
    # print substrate_network.all_shortest_paths()
    print "shortestpath"
    print substrate_network.get_shortest_paths(1,7,weight='latency')
    path = substrate_network.get_minimum_latency_path(1, 5)
    print path
    print substrate_network.get_minimum_free_bandwidth(path)
    print "single source"
    print substrate_network.get_single_source_minimum_latency_path(2)
    print substrate_network.edges().data()
    substrate_network.allocate_bandwidth_resource_path(path, 10)
    print substrate_network.edges().data()
    print "Finished"


