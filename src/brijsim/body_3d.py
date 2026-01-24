from attr import dataclass


@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def abs(self) -> "Vector3":
        return Vector3(abs(self.x), abs(self.y), abs(self.z))


class Body3D:
    def __init__(self, position: Vector3 = Vector3(0, 0, 0), mass: float = 0.0):
        self.position = position
        self.mass = mass
