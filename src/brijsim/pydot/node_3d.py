from brijsim.pydot.transform_3d import Transform3D
from brijsim.pydot.vector3 import Vector3

from .node import Node

# todo If I come back to this, consider https://github.com/Wasserwecken/spatial-transform


class Node3D(Node):
    def __init__(self, name: str):
        super().__init__(name)
        self.transform = Transform3D()

    @property
    def position(self):
        return self.transform.origin

    @position.setter
    def position(self, value: Vector3):
        self.transform.origin = value
