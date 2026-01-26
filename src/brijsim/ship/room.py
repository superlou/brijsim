from brijsim.body_3d import Body3D, Shape3D, Vector3
from brijsim.devices.device import Device


class Room(Body3D):
    def __init__(self, position: Vector3, mass: float, shape: Shape3D):
        super().__init__(position, mass, shape)
        self.devices: list[Device] = []
        self.parent: "Ship" | None = None

    def add_device(self, device: Device):
        self.devices.append(device)
        for port_name, port in device.flow_ports.items():
            self.parent.flow_model.add_port(f"{device.name}:{port_name}", port)

        return device
