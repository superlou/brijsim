from typing import ClassVar, Self

from attr import dataclass

from brijsim.node import Node


@dataclass
class Vector3:
    x: float
    y: float
    z: float
    ZERO: ClassVar["Vector3"]

    def abs(self) -> "Vector3":
        return Vector3(abs(self.x), abs(self.y), abs(self.z))


Vector3.ZERO = Vector3(0, 0, 0)


class Shape3D:
    pass


class EmptyShape3D(Shape3D):
    def __init__(self):
        self.size = Vector3.ZERO


class BoxShape3D(Shape3D):
    def __init__(self, size: Vector3):
        self.size = size


class Body3D(Node):
    def __init__(
        self,
        position: Vector3 = Vector3.ZERO,
        mass: float = 0.0,
        shape: Shape3D = EmptyShape3D(),
        rotation: Vector3 = Vector3.ZERO,
    ):
        self.position = position
        self.mass = mass
        self.shape = shape
        self.rotation = rotation
