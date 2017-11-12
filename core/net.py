from networkx import networkx as nx
from basic_object import BasicObject
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
        return self._get_link_attribute(u,v, 'bandwidth_free')
    def reset_bandwidth_capacity(self,u,v, bw_c):
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



if __name__ == '__main__':
    g = Net()
    g.add_node(1)
    g.add_node(2)
    g.set_link_bandwidth_capacity(1, 2, 100)
    print g.get_link_bandwidth_capacity(1, 2)
    print g.edges[2, 1]['bandwidth_capacity']
    print g[2][1]['bandwidth_capacity']
    print g[1][2]['bandwidth_capacity']
    print g.nodes().data()
    print g.edges().data()

