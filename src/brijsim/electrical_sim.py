from dataclasses import dataclass, field
from typing import Self

import numpy as np


@dataclass
class Component:
    name: str


@dataclass
class Link:
    component: Component
    pin: str


@dataclass
class Resistor(Component):
    resistance: float

    @property
    def conductance(self) -> float:
        return 1 / self.resistance


@dataclass
class Node:
    id: int
    voltage: float = 0.0
    links: list[Link] = field(default_factory=list)

    def link(self, component: Component, pin: str) -> Self:
        self.links.append(Link(component, pin))
        return self

    def spanning_components(self, other_node: Self) -> list[Component]:
        # todo This will have a problem if a component has more than three terminals,
        # i.e., p isn't matched to n
        p_components = [link.component for link in self.links if link.pin == "p"]
        n_components = [link.component for link in self.links if link.pin == "n"]
        return [
            link.component
            for link in other_node.links
            if (link.component in p_components and link.pin == "n")
            or (link.component in n_components and link.pin == "p")
        ]


@dataclass
class IndVoltageSource(Component):
    voltage: float = 0.0
    current: float = 0.0


@dataclass
class IndCurrentSource(Component):
    voltage: float = 0.0
    current: float = 0.0


class ElectricalNetwork:
    def __init__(self):
        self.nodes: list[Node] = [Node(0)]
        self.ind_voltage_sources: list[IndVoltageSource] = []
        self.ind_current_sources: list[IndCurrentSource] = []
        self.resistors: dict[str, Resistor] = {}

    def add_ind_voltage_source(self, name: str, np: int, nn: int, voltage: float):
        source = IndVoltageSource(name=name, voltage=voltage)
        self.get_node(np).link(source, "p")
        self.get_node(nn).link(source, "n")
        self.ind_voltage_sources.append(source)

    def add_ind_current_source(self, name: str, np: int, nn: int, current: float):
        source = IndCurrentSource(name=name, current=current)
        self.get_node(np).link(source, "p")
        self.get_node(nn).link(source, "n")
        self.ind_current_sources.append(source)

    def add_resistor(self, name: str, np: int, nn: int, resistance: float):
        resistor = Resistor(name, resistance)
        self.get_node(np).link(resistor, "p")
        self.get_node(nn).link(resistor, "n")
        self.resistors[name] = resistor

    def get_node(self, id: int) -> Node:
        while id >= len(self.nodes):
            self.nodes.append(Node(len(self.nodes)))

        return self.nodes[id]

    def build_G(self) -> np.ndarray:
        # G is the conductance matrix
        # Diagonals: sum of conductance connected to each node
        # Others: negative of conductance spanning node pairs
        # todo What about when two resistors are in parallel?
        n = len(self.nodes) - 1  # ignore node 0
        G = np.zeros((n, n))

        for iy, ix in np.ndindex(G.shape):
            if iy == ix:
                node = self.nodes[iy + 1]
                G[iy, ix] = sum(
                    link.component.conductance
                    for link in node.links
                    if isinstance(link.component, Resistor)
                )
            else:
                node_a = self.nodes[iy + 1]
                node_b = self.nodes[ix + 1]
                G[iy, ix] = sum(
                    -component.conductance
                    for component in node_a.spanning_components(node_b)
                    if isinstance(component, Resistor)
                )

        return G

    def build_B(self) -> np.ndarray:
        # B identifies which independent voltage sources are into or out of
        # each node.
        n = len(self.nodes) - 1  # ignore node 0
        m = len(self.ind_voltage_sources)
        B = np.zeros((n, m))

        for node in self.nodes[1:]:
            for link in node.links:
                if not isinstance(link.component, IndVoltageSource):
                    continue

                i = node.id - 1
                j = self.ind_voltage_sources.index(link.component)
                B[i, j] = 1 if link.pin == "p" else -1

        return B

    def build_C(self) -> np.ndarray:
        # todo Only when there are no dependent voltage sources
        return self.build_B().T

    def build_D(self) -> np.ndarray:
        # todo Only when there are no dependent sources
        m = len(self.ind_voltage_sources)
        return np.zeros((m, m))

    def build_i(self) -> np.ndarray:
        # For each node, the sum of currents into that node
        i = []
        for node in self.nodes[1:]:
            total = 0
            for link in node.links:
                if isinstance(link.component, IndCurrentSource):
                    sign = 1 if link.pin == "p" else -1
                    total += sign * link.component.current

            i.append(total)

        return np.array(i)

    def build_e(self) -> np.ndarray:
        # Voltages of independent voltage sources
        return np.array([ivs.voltage for ivs in self.ind_voltage_sources])

    def run(self):
        # based on https://lpsa.swarthmore.edu/Systems/Electrical/mna/MNA3.html
        G = self.build_G()
        B = self.build_B()
        C = self.build_C()
        D = self.build_D()
        A = np.block([[G, B], [C, D]])

        # todo This doesn't account for independent current sources
        i = self.build_i()
        e = self.build_e()
        z = np.concat([i, e])

        x = np.matmul(np.linalg.inv(A), z)

        num_nodes = len(self.nodes) - 1

        for node in self.nodes[1:]:
            node.voltage = x[node.id - 1]

        for i, source in enumerate(self.ind_voltage_sources):
            source.current = x[i + num_nodes]
