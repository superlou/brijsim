from collections.abc import Callable
from typing import Any

from brijsim.flow_sim import FlowPort


class Element:
    def __init__(self, name: str):
        self.name = name
        self.flow_ports: dict[str, FlowPort] = {}
        self.actions: dict[str, Callable[[], Any]] = {}
        self.state = None

    def process(self, dt: float):
        pass
