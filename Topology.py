import Utilities

class Topology:
    topology = None
    flat_topology = None
    count = None

    def __init__(self, topology, count):
        if type(topology) is str:
            self.topology = topology
            self.flat_topology = Utilities.flatten(self.topology)
        if type(count) is int:
            self.count = count


