import unittest
from core.node import Node
from core.substrate_node import SubstrateNode
from core.net import Net
from core.vnf import VNF


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.node = Node()
        self.substrate_node = SubstrateNode(200)
        self.net = Net()
        self.vnf = VNF('test')
    def test_Node(self):
        self.assertEqual(self.node.test_function(), "test function: Node")

    def test_substrate_node(self):
        self.assertEqual(self.substrate_node.get_id(), 200)
        self.assertEqual(self.substrate_node.set_cpu_capacity(100), 100)
        self.assertEqual(self.substrate_node.get_cpu_free(), 100)
        self.assertEqual(self.substrate_node.get_cpu_capacity(), 100)
        self.assertEqual(self.substrate_node.allocate_cpu_resource(20), 20)
        self.assertEqual(self.substrate_node.get_cpu_used(), 20)
        self.assertEqual(self.substrate_node.get_cpu_free(), 80)
        self.substrate_node.reset()
        self.assertEqual(self.substrate_node.get_cpu_capacity(), 100)
        self.assertEqual(self.substrate_node.get_cpu_free(), 100)
        self.assertEqual(self.substrate_node.get_cpu_used(), 0)
        self.substrate_node.reset_with_cpu_capacity(200)
        self.assertEqual(self.substrate_node.get_cpu_capacity(), 200)
        self.assertEqual(self.substrate_node.get_cpu_used(), 0)
        self.assertEqual(self.substrate_node.get_cpu_free(), 200)
        self.assertEqual(self.substrate_node.allocate_cpu_resource(150), 150)
        self.assertEqual(self.substrate_node.get_cpu_capacity(), 200)
        self.assertEqual(self.substrate_node.get_cpu_free(), 50)
        self.assertEqual(self.substrate_node.get_cpu_used(), 150)

    def test_net_node(self):
        self.net.init_node_cpu_capacity(1, 100)
        self.assertEqual(self.net.get_node_cpu_capacity(1), 100)
        self.assertEqual(self.net.get_node_cpu_free(1), 100)
        self.assertEqual(self.net.get_node_cpu_used(1), 0)
        self.assertTrue(self.net.allocate_cpu_resource(1, 10))
        self.assertEqual(self.net.get_node_cpu_capacity(1), 100)
        self.assertEqual(self.net.get_node_cpu_free(1), 90)
        self.assertEqual(self.net.get_node_cpu_used(1), 10)
        self.assertFalse(self.net.allocate_cpu_resource(1, 95))
        self.net.reset_node_cpu_capacity(1, 100)
        self.assertEqual(self.net.get_node_cpu_capacity(1), 100)
        self.assertEqual(self.net.get_node_cpu_free(1), 100)
        self.assertEqual(self.net.get_node_cpu_used(1), 0)
        self.assertEqual(1, 1)

    def test_net_link(self):
        self.net.init_bandwidth_capacity(1, 2, 100)
        self.assertEqual(self.net.get_link_bandwidth_capacity(1, 2), 100)
        self.assertEqual(self.net.get_link_bandwidth_used(1, 2), 0)
        self.assertEqual(self.net.get_link_bandwidth_free(1, 2), 100)
        self.assertTrue(self.net.allocate_bandwidth_resource(1, 2, 80))
        self.assertFalse(self.net.allocate_bandwidth_resource(1, 2, 90))
        self.assertEqual(self.net.get_link_bandwidth_used(1, 2), 80)
        self.assertEqual(self.net.get_link_bandwidth_free(1, 2), 20)
        self.net.init_link_latency(1, 2, 2)
        self.assertEqual(self.net.get_link_latency(1, 2,), 2)
        pass
    def test_vnf(self):
        self.vnf.set_cpu_request(100)
        self.assertEqual(self.vnf.get_cpu_request(), 100)
        self.vnf.set_income_interface_bandwidth(105)
        self.assertEqual(self.vnf.get_income_interface_bandwidth(), 105)
        self.vnf.set_outcome_interface_banwdith(110)
        self.assertEqual(self.vnf.get_outcome_interface_bandwidth(), 110)
        vnf2 = VNF(2)
        vnf3 = VNF(3)
        self.vnf.set_next_vnf(vnf2)
        self.vnf.set_previous_vnf(vnf3)
        self.assertEqual(self.vnf.get_previous_vnf().id, 3)
        self.assertEqual(self.vnf.get_next_vnf().id, 2)


        pass

if __name__ == '__main__':
    unittest.main()
