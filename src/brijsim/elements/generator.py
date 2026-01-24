from enum import StrEnum, auto

from brijsim.elements.element import Element
from brijsim.flow_sim import FlowPort


class FusionGeneratorState(StrEnum):
    OFF = auto()
    STARTING = auto()
    RUNNING = auto()


class FusionGenerator(Element):
    def __init__(self, name: str):
        super().__init__(name)
        self.flow_ports = {"src": FlowPort(0.0, 0.0), "boost": FlowPort(0.0, 0.0)}
        self.actions = {"start": self.start}
        self.state = FusionGeneratorState.OFF

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


class AuxGenerator(Element):
    def __init__(self, name: str, rate_capacity: float):
        super().__init__(name)
        self.flow_ports = {
            "src": FlowPort(0.0, 0.0),
            "fuel": FlowPort(0.0, 0.0, rate_unit="kg/h", qty_unit="kg"),
        }
        self.actions = {"start": self.start, "stop": self.stop}
        self.state = SimpleGeneratorState.OFF
        self.rate_capacity = rate_capacity
        self.level: float = 0.0

    def start(self):
        self.state = SimpleGeneratorState.STARTING

    def stop(self):
        self.state = SimpleGeneratorState.STOPPING

    def process(self, dt: float):
        match self.state:
            case SimpleGeneratorState.STARTING:
                self.flow_ports["fuel"].rate_capacity = -350.0 * self.level

                self.level += 0.5 * dt
                if self.level >= 1.0:
                    self.level = 1.0
                    self.state = SimpleGeneratorState.RUNNING

                self.flow_ports["src"].rate_capacity = self.level * self.rate_capacity
            case SimpleGeneratorState.STOPPING:
                self.level -= 0.5 * dt
                if self.level <= 0.0:
                    self.level = 0.0
                    self.state = SimpleGeneratorState.OFF

                self.flow_ports["fuel"].rate_capacity = -350.0 * self.level

                self.flow_ports["src"].rate_capacity = self.level * self.rate_capacity
