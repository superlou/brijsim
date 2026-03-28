from networkx.classes.digraph import DiGraph

from brijsim.pydot import Node, Node3D
from brijsim.universe.region import Region


class Universe(Node):
    def __init__(self, name):
        super().__init__(name)
        self.network = DiGraph()

    def add_region(self, region: Region):
        super().add_child(region)
        self.network.add_node(region.name, region=region)


class Wormhole(Node):
    def __init__(self, name):
        super().__init__(name)
        self.entrance = WormholeEntrance(f"{name}-entrance")
        self.exit = WormholeExit(f"{name}-exit")


class WormholeEntrance(Node3D):
    pass


class WormholeExit(Node3D):
    pass
