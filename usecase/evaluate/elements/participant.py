from usecase.evaluate.elements.base_element import BaseElement
from usecase.evaluate.utils import Element


class Lane(BaseElement):
    event_sub_process: list
    node: list

    def __init__(self, element: Element):
        super().__init__(element)
        self.event_sub_process = []
        self.node = []

    def accept(self, t, c, r):
        return t.visit_for_Lane(self, c, r)


class Participant(BaseElement):
    lane: list
    node: list

    def __init__(self, element: Element):
        super().__init__(element)
        self.lane = []
        self.node = []

    def accept(self, t, c, r):
        return t.visit_for_Participant(self, c, r)
