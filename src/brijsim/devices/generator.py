from enum import StrEnum, auto

from brijsim.devices.device import Device
from brijsim.flow_sim import FlowPort


class FusionGeneratorState(StrEnum):
    OFF = auto()
    STARTING = auto()
    RUNNING = auto()


class FusionGenerator(Device):
    def __init__(self, name: str):
        super().__init__(name)
        self.flow_ports = {"src": FlowPort(0.0, 0.0), "boost": FlowPort(0.0, 0.0)}
        self.state = FusionGeneratorState.OFF

    @Device.action
    def start(self):
        if self.state != FusionGeneratorState.OFF:
            return

        self.flow_ports["boost"].rate_capacity = -50
        self.state = FusionGeneratorState.STARTING

    def process(self, dt: float):
        match self.state:
            case FusionGeneratorState.STARTING:
                if self.flow_ports["boost"].at_p_capacity():
                    self.state = FusionGeneratorState.RUNNING
                    self.flow_ports["boost"].rate_capacity = 0
                    self.flow_ports["src"].rate_capacity = 100.0


class SimpleGeneratorState(StrEnum):
    OFF = auto()
    STARTING = auto()
    STOPPING = auto()
    RUNNING = auto()


class AuxGenerator(Device):
    def __init__(self, name: str, rate_capacity: float):
        super().__init__(name)
        self.flow_ports = {
            "src": FlowPort(0.0, 0.0),
            "fuel": FlowPort(0.0, 0.0, rate_unit="kg/s", qty_unit="kg"),
        }
        self.state = SimpleGeneratorState.OFF
        self.rate_capacity = rate_capacity
        self.level: float = 0.0

    @Device.action
    def start(self):
        self.state = SimpleGeneratorState.STARTING

    @Device.action
    def stop(self):
        self.state = SimpleGeneratorState.STOPPING

    def process(self, dt: float):
        match self.state:
            case SimpleGeneratorState.STARTING:
                self.level += 0.5 * dt
                if self.level >= 1.0:
                    self.level = 1.0
                    self.state = SimpleGeneratorState.RUNNING
            case SimpleGeneratorState.STOPPING:
                self.level -= 0.5 * dt
                if self.level <= 0.0:
                    self.level = 0.0
                    self.state = SimpleGeneratorState.OFF

        self.flow_ports["fuel"].rate_capacity = -2000.0 * self.level
        self.flow_ports["src"].rate_capacity = (
            self.level * self.rate_capacity * self.flow_ports["fuel"].rate_fraction
        )
