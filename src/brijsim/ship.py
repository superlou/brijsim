from brijsim.elements.element import Element
from brijsim.flow_sim import FlowModel


class Ship:
    def __init__(self):
        self.elements: list[Element] = []
        self.e_model = FlowModel()

    def add_element(self, element: Element):
        self.elements.append(element)
        for name, port in element.flow_ports.items():
            self.e_model.add_port(port)

    def process(self, dt: float):
        self.e_model.step(dt)
        for element in self.elements:
            element.process(dt)
