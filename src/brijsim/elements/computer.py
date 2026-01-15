from brijsim.elements.element import Element
from brijsim.energy_sim import EPort


class JumpComputer(Element):
    def __init__(self, name: str):
        super().__init__(name)
        self.e_ports = {"pwr": EPort(-20.0, 0.0)}
        self.state = False

    def process(self, dt: float):
        self.state = str(self.e_ports["pwr"].at_p_capacity())
