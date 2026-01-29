from brijsim.devices.device import Device
from brijsim.flow_sim import FlowModel
from brijsim.ship.room import Room

from ..pydot import Body3D, Node


class Ship(Body3D):
    def __init__(self, name: str):
        self.flow_model = FlowModel()
        super().__init__(name)

    def add_child(self, child: Node):
        super().add_child(child)

        if isinstance(child, Device):
            for port_name, port in child.flow_ports.items():
                self.flow_model.add_port(f"{child.name}:{port_name}", port)

    @property
    def rooms(self) -> list[Room]:
        return self.get_children_by_type(Room)

    @property
    def devices(self) -> list[Device]:
        return self.get_children_by_type(Device)

    def link_ports(self, port1_id: str, port2_id: str):
        self.flow_model.link_ports(port1_id, port2_id)

    def process(self, delta: float):
        self.flow_model.step(delta)

    def find_room_by_name(self, name: str) -> Room:
        return [room for room in self.rooms if room.name == name][0]
