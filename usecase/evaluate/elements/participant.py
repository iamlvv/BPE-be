from usecase.evaluate.elements.base_element import BaseElement
from usecase.evaluate.utils import Element


class Lane(BaseElement):
    eventSubProcess: list
    node: list

    def __init__(self, element: Element):
        super().__init__(element)
        self.eventSubProcess = []
        self.node = []

    def accept(self, t, c, r):
        return t.visitForLane(self, c, r)


class Pool(BaseElement):
    lane: list

    def __init__(self, element: Element):
        super().__init__(element)
        self.lane = []

    def accept(self, t, c, r):
        return t.visitForPool(self, c, r)
