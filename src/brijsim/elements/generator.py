from enum import StrEnum, auto

from brijsim.elements.element import Element
from brijsim.energy_sim import EPort


class FusionGeneratorState(StrEnum):
    OFF = auto()
    STARTING = auto()
    RUNNING = auto()


class FusionGenerator(Element):
    def __init__(self, name: str):
        super().__init__(name)
        self.e_ports = {"src": EPort(0.0, 0.0), "boost": EPort(0.0, 0.0)}
        self.actions = {"start": self.start}
        self.state = FusionGeneratorState.OFF

    def start(self):
        if self.state != FusionGeneratorState.OFF:
            return

        self.e_ports["boost"].p_capacity = -50
        self.state = FusionGeneratorState.STARTING

    def process(self, dt: float):
        match self.state:
            case FusionGeneratorState.STARTING:
                if self.e_ports["boost"].at_p_capacity():
                    self.state = FusionGeneratorState.RUNNING
                    self.e_ports["boost"].p_capacity = 0
                    self.e_ports["src"].p_capacity = 100.0


class SimpleGeneratorState(StrEnum):
    OFF = auto()
    STARTING = auto()
    STOPPING = auto()
    RUNNING = auto()


class AuxGenerator(Element):
    def __init__(self, name: str, p_capacity: float):
        super().__init__(name)
        self.e_ports = {"src": EPort(0.0, 0.0)}
        self.actions = {"start": self.start, "stop": self.stop}
        self.state = SimpleGeneratorState.OFF
        self.p_capacity = p_capacity
        self.level: float = 0.0

    def start(self):
        self.state = SimpleGeneratorState.STARTING

    def stop(self):
        self.state = SimpleGeneratorState.STOPPING

    def process(self, dt: float):
        match self.state:
            case SimpleGeneratorState.STARTING:
                self.level += 0.5 * dt
                if self.level >= 1.0:
                    self.level = 1.0
                    self.state = SimpleGeneratorState.RUNNING

                self.e_ports["src"].p_capacity = self.level * self.p_capacity
            case SimpleGeneratorState.STOPPING:
                self.level -= 0.5 * dt
                if self.level <= 0.0:
                    self.level = 0.0
                    self.state = SimpleGeneratorState.OFF

                self.e_ports["src"].p_capacity = self.level * self.p_capacity
