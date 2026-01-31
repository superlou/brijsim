from typing import ClassVar

from attr import dataclass


@dataclass
class Vector3:
    x: float
    y: float
    z: float
    ZERO: ClassVar["Vector3"]

    def abs(self) -> "Vector3":
        return Vector3(abs(self.x), abs(self.y), abs(self.z))


Vector3.ZERO = Vector3(0, 0, 0)
