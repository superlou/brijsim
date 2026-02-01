import glm
from SpatialTransform import Transform

from brijsim.pydot.vector3 import Vector3

from .node import Node


class Node3D(Node):
    def __init__(self, name: str):
        super().__init__(name)
        self.transform: Transform = Transform(self.name)

    def add_child(self, child: Node):
        super().add_child(child)
        if isinstance(child, Node3D):
            # https://github.com/Wasserwecken/spatial-transform/issues/4
            position = child.transform.Position
            self.transform.attach(child.transform)
            child.transform.Position = position

    @property
    def position(self) -> Vector3:
        return Vector3(
            self.transform.Position.x,
            self.transform.Position.y,
            self.transform.Position.z,
        )

    @position.setter
    def position(self, value: Vector3):
        self.transform.Position = glm.vec3(value.x, value.y, value.z)

    @property
    def global_position(self) -> Vector3:
        return Vector3(
            self.transform.PositionWorld.x,
            self.transform.PositionWorld.y,
            self.transform.PositionWorld.z,
        )

    @global_position.setter
    def global_position(self, value: Vector3):
        self.transform.PositionWorld = glm.vec3(value.x, value.y, value.z)
