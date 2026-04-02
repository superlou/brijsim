from typing import Type, TypeVar

from .node import Node

T = TypeVar("T")


class SceneTree:
    def __init__(self):
        self.root = SceneTreeRoot("root", self)
        self.process_time = 0.0
        self.node_uuid_map: dict[str, Node] = {}

    def add_child(self, child: Node):
        self.root.add_child(child)

    def process(self, delta: float):
        for child in self.root.children:
            self._process_child(child, delta)

        self.process_time += delta

    def _process_child(self, child: Node, delta: float):
        for _child in child.children:
            self._process_child(_child, delta)

        child.process(delta)

    def find_nodes_by_type(
        self, type_: Type[T], current: Node | None = None, found: set[T] | None = None
    ) -> set[T]:
        if current is None:
            current = self.root

        if found is None:
            found = set([])

        if isinstance(current, type_):
            found.add(current)

        for child in current.children:
            self.find_nodes_by_type(type_, child, found)

        return found


class SceneTreeRoot(Node):
    def __init__(self, name: str, scene_tree: SceneTree):
        super().__init__(name)
        self.scene_tree = scene_tree
