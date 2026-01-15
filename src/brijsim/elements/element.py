from collections.abc import Callable
from typing import Any

from brijsim.energy_sim import EPort


class Element:
    def __init__(self, name: str):
        self.name = name
        self.e_ports: dict[str, EPort] = {}
        self.actions: dict[str, Callable[[], Any]] = {}
        self.state = None

    def process(self, dt: float):
        pass
