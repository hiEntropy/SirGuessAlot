class Topology:
    topology = None
    count = None

    def __init__(self, topology, count):
        if type(topology) is str:
            self.topology = topology
        if type(count) is int:
            self.count = count
    def get_count(self):
        return self.count
