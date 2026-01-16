from brijsim.elements.element import Element
from brijsim.flow_sim import FlowPort


class JumpComputer(Element):
    def __init__(self, name: str):
        super().__init__(name)
        self.flow_ports = {"pwr": FlowPort(-20.0, 0.0)}
        self.state = False

    def process(self, dt: float):
        self.state = str(self.flow_ports["pwr"].at_p_capacity())
