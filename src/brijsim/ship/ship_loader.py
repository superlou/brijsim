from pathlib import Path

import yaml

from brijsim.devices.computer import JumpComputer
from brijsim.devices.generator import AuxGenerator, FusionGenerator
from brijsim.devices.hatch import Hatch
from brijsim.devices.tanks import FuelTank
from brijsim.ship.room import Room
from brijsim.ship.ship import Ship

from ..pydot import BoxShape3D, Vector3


class ShipLoader:
    def load(self, filename: str | Path) -> Ship:
        file_path = Path(filename)

        data = yaml.load(file_path.read_text(), Loader=yaml.Loader)

        ship = Ship(data["name"])

        for room_data in data["rooms"]:
            name = room_data["name"]
            position = Vector3(*room_data["position"])
            mass = room_data.get("mass", 0.0)
            size = Vector3(*room_data["shape"]["size"])
            shape = BoxShape3D(size)

            room = Room(name, position, mass, shape)
            ship.add_child(room)

        for room_data in data["rooms"]:
            room = ship.find_room_by_name(room_data["name"])

            for device_data in room_data.get("devices", []):
                name = device_data["name"]
                match device_data["type"]:
                    case "JumpComputer":
                        device = JumpComputer(name)
                    case "FusionGenerator":
                        device = FusionGenerator(name)
                    case "AuxGenerator":
                        rate_capacity = device_data["rate_capacity"]
                        device = AuxGenerator(name, rate_capacity)
                    case "FuelTank":
                        device = FuelTank(
                            name, device_data["qty_max"], device_data["qty"]
                        )
                    case "Hatch":
                        device = Hatch(
                            name,
                            [
                                ship.find_room_by_name(name)
                                for name in device_data["linked_rooms"]
                            ],
                        )
                    case _:
                        device = None

                if device:
                    room.add_child(device)

        for port1, port2 in data["port_links"]:
            ship.link_ports(port1, port2)

        return ship
