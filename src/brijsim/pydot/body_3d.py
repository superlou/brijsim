from .node_3d import Node3D
from .vector3 import Vector3


class Shape3D:
    pass


class EmptyShape3D(Shape3D):
    def __init__(self):
        self.size = Vector3.ZERO


class BoxShape3D(Shape3D):
    def __init__(self, size: Vector3):
        self.size = size


class Body3D(Node3D):
    def __init__(
        self,
        name: str,
        position: Vector3 = Vector3.ZERO,
        mass: float = 0.0,
        shape: Shape3D = EmptyShape3D(),
        rotation: Vector3 = Vector3.ZERO,
    ):
        super().__init__(name)
        self.position = position
        self.mass = mass
        self.shape = shape
        self.rotation = rotation
