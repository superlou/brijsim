class Node:
    def __init__(self, name: str):
        self.name = name
        self.parent = None
        self.children: list[Node] = []

    def add_child(self, child: "Node"):
        if child not in self.children:
            self.children.append(child)
            child.parent = self

    def process(self, delta: float):
        pass
