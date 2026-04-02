import json
from dataclasses import dataclass
from uuid import UUID

from inflection import dasherize, underscore


class Widget:
    def __init__(self):
        self.component = dasherize(underscore(self.__class__.__name__))
        self.data = []

    def to_dict(self) -> dict:
        return {
            "component": self.component,
            "data": self.data,
        }


class LabeledString(Widget):
    def __init__(self, label: str, value: str, level: str = "normal"):
        super().__init__()
        self.data = {"label": label, "value": value, "level": level}


class DeviceButton(Widget):
    def __init__(self, label: str, action: str):
        super().__init__()
        self.data = {"label": label, "action": action}


class DeviceBarGauge(Widget):
    def __init__(self, label: str, value: float, max: float):
        super().__init__()
        self.data = {"label": label, "value": value, "max": max}


@dataclass
class Panel:
    device_uuid: str
    name: str
    widgets: list[Widget]

    def to_dict(self) -> dict:
        return {
            "device_uuid": self.device_uuid,
            "name": self.name,
            "widgets": [w.to_dict() for w in self.widgets],
        }
