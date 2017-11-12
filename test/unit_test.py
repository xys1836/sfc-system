import unittest
from core.node import Node
from core.substrate_node import SubstrateNode



class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.node = Node()
        self.substrate_node = SubstrateNode(200)
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



if __name__ == '__main__':
    unittest.main()
