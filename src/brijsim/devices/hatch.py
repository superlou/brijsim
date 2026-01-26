from enum import StrEnum, auto

from brijsim.devices.device import Device
from brijsim.ship.room import Room


class HatchState(StrEnum):
    CLOSED = auto()
    OPENED = auto()
    LOCKED_CLOSED = auto()
    LOCKED_OPENED = auto()


class Hatch(Device):
    def __init__(self, name, linked_rooms: list[Room]):
        super().__init__(name)
        self.state = HatchState.CLOSED

    @Device.action
    def open(self):
        self.state = HatchState.OPENED

    @Device.action
    def close(self):
        self.state = HatchState.CLOSED
