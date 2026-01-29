from brijsim.devices.device import Device

from ..pydot import Body3D, Node


class Room(Body3D):
    def add_child(self, child: Node):
        super().add_child(child)

        if isinstance(child, Device):
            for port_name, port in child.flow_ports.items():
                self.parent.flow_model.add_port(f"{child.name}:{port_name}", port)

    @property
    def devices(self) -> list[Device]:
        return [child for child in self.children if isinstance(child, Device)]
