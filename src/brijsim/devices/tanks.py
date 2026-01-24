from enum import StrEnum, auto

from brijsim.devices.device import Device
from brijsim.flow_sim import FlowPort


class FuelTank(Device):
    def __init__(self, name: str, max_qty: float, initial_qty: float = 0.0):
        super().__init__(name)
        self.max_qty = max_qty
        self.flow_ports = {
            "fuel": FlowPort(
                0.0, max_qty, qty=initial_qty, rate_unit="kg/s", qty_unit="kg"
            )
        }
