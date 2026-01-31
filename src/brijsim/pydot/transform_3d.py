import numpy as np

from brijsim.pydot.vector3 import Vector3


class Transform3D:
    def __init__(self):
        self.basis = Basis()
        self.origin = Vector3.ZERO


class Basis:
    def __init__(self):
        self.m = np.array(
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
            ]
        )
