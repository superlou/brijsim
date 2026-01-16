from brijsim.elements.element import Element
from brijsim.flow_sim import FlowModel, FlowPort


class Ship:
    def __init__(self):
        self.elements: list[Element] = []
        self.flow_model = FlowModel()

    def add_element(self, element: Element):
        self.elements.append(element)
        for port_name, port in element.flow_ports.items():
            self.flow_model.add_port(port, f"{element.name}:{port_name}")

    def link_ports(self, port1: str, port2: str):
        self.flow_model.graph.add_edge(port1, port2)

    def process(self, dt: float):
        self.flow_model.step(dt)
        for element in self.elements:
            element.process(dt)
