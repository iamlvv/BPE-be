from usecase.evaluate.elements.base_element import BaseElement
from usecase.evaluate.utils import Element


class Activity(BaseElement):
    boundary: list

    def __init__(self, element: Element):
        super().__init__(element)
        self.boundary = element.boundary
