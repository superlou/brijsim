import uuid
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from brijsim.pydot.scene_tree import SceneTree


class Node:
    def __init__(self, name: str):
        self.uuid = uuid.uuid4().hex
        self.name = name
        self.parent = None
        self.children: list[Node] = []
        self.scene_tree: SceneTree | None = None

    def add_child(self, child: "Node"):
        if child in self.children:
            return

        self.children.append(child)
        child.parent = self

        if self.scene_tree:
            self._recursively_add_to_scene_tree(child)

        child.scene_tree = self.scene_tree

    def _recursively_add_to_scene_tree(self, node: Self):
        self.scene_tree.node_uuid_map[node.uuid] = node
        node.scene_tree = self.scene_tree

        for child in node.children:
            self._recursively_add_to_scene_tree(child)

    def process(self, delta: float):
        pass

    def get_children_by_type[T](self, type_: type[T]) -> list[T]:
        return [child for child in self.children if isinstance(child, type_)]
