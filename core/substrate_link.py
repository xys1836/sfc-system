from link import Link
class SubstrateLink(Link):
    def __init__(self):
        self.v1 = None
        self.v2 = None
        self.bandwidth_capacity = 0
        self.bandwidth__used = 0
        self.bandwidth__free = 0

