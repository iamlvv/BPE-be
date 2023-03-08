from usecase.evaluate.elements.node import Node
from usecase.evaluate.utils import Element


class Activity(Node):
    boundary: list

    def __init__(self, element: Element):
        super().__init__(element)
        # self.boundary = element.boundary
