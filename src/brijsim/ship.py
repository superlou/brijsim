from brijsim.body_3d import Body3D
from brijsim.devices.device import Device
from brijsim.flow_sim import FlowModel


class Ship(Body3D):
    def __init__(self):
        self.device: list[Device] = []
        self.flow_model = FlowModel()
        super().__init__()

    def add_device(self, device: Device):
        self.device.append(device)
        for port_name, port in device.flow_ports.items():
            self.flow_model.add_port(f"{device.name}:{port_name}", port)

        return device

    def link_ports(self, port1_id: str, port2_id: str):
        self.flow_model.link_ports(port1_id, port2_id)

    def process(self, dt: float):
        self.flow_model.step(dt)
        for element in self.device:
            element.process(dt)
