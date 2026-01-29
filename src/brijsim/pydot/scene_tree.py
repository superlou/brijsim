from .node import Node


class SceneTree:
    def __init__(self):
        self.root = SceneTreeRoot("root")
        self.process_time = 0.0

    def add_child(self, child: "Node"):
        self.root.add_child(child)

    def process(self, delta: float):
        for child in self.root.children:
            self._process_child(child, delta)

        self.process_time += delta

    def _process_child(self, child: Node, delta: float):
        for _child in child.children:
            self._process_child(_child, delta)

        child.process(delta)


class SceneTreeRoot(Node):
    pass
