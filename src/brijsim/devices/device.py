import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any

from brijsim.body_3d import Body3D
from brijsim.flow_sim import FlowPort


class Device(Body3D):
    def __init__(self, name: str):
        self.name = name
        self.flow_ports: dict[str, FlowPort] = {}
        self.state = None
        super().__init__()

    def process(self, dt: float):
        pass

    @staticmethod
    def action(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        wrapper._is_action = True
        return wrapper

    @property
    def actions(self):
        d = {
            name: member
            for name, member in inspect.getmembers_static(self, inspect.isfunction)
            if hasattr(member, "_is_action") and member._is_action
        }
        return d
