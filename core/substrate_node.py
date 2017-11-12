from node import Node
class SubstrateNode(Node):
    def __init__(self, id):
        self.id = id
        self.cpu_capacity = None
        self.cpu_used = 0
        self.cpu_free = 0

    def reset(self):
        self.cpu_used = 0
        self.cpu_free = self.cpu_capacity

    def reset_with_cpu_capacity(self, cpu_capacity):
        self.cpu_capacity = cpu_capacity
        self.cpu_free = self.cpu_capacity
        self.cpu_used = 0

    def _set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_cpu_capacity(self, cpu_capacity):
        self.cpu_capacity = cpu_capacity
        self.cpu_free = cpu_capacity
        self.cpu_used = 0
        return self.cpu_capacity

    def get_cpu_capacity(self):
        return self.cpu_capacity

    def get_cpu_used(self):
        return self.cpu_used

    def _set_cpu_used(self, cpu_used):
        if cpu_used < self.cpu_capacity:
            self.cpu_used = cpu_used
        return self.cpu_used
    def get_cpu_free(self):
        return self.cpu_free

    def allocate_cpu_resource(self, cpu_amount_to_allocated):
        if cpu_amount_to_allocated > self.cpu_free:
           raise("CPU resources cannot be allocated. No enough resources to be allcoated")
        else:
           self.cpu_free = self.cpu_free - cpu_amount_to_allocated
           self.cpu_used = self.cpu_used + cpu_amount_to_allocated
        return cpu_amount_to_allocated


