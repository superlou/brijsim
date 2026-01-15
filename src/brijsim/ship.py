from brijsim.elements.element import Element
from brijsim.energy_sim import ElectricalEnergyModel


class Ship:
    def __init__(self):
        self.elements: list[Element] = []
        self.e_model = ElectricalEnergyModel()

    def add_element(self, element: Element):
        self.elements.append(element)
        for name, port in element.e_ports.items():
            self.e_model.add_port(port)

    def process(self, dt: float):
        self.e_model.step(dt)
        for element in self.elements:
            element.process(dt)
