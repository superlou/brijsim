from brijsim.body_3d import Body3D
from brijsim.devices.device import Device
from brijsim.flow_sim import FlowModel, FlowPort


class Ship(Body3D):
    def __init__(self):
        self.elements: list[Device] = []
        self.flow_model = FlowModel()
        super().__init__()

    def add_element(self, element: Device):
        self.elements.append(element)
        for port_name, port in element.flow_ports.items():
            self.flow_model.add_port(f"{element.name}:{port_name}", port)

        return element

    def link_ports(self, port1_id: str, port2_id: str):
        self.flow_model.link_ports(port1_id, port2_id)

    def process(self, dt: float):
        self.flow_model.step(dt)
        for element in self.elements:
            element.process(dt)
