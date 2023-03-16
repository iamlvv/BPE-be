from usecase.evaluate.elements.base_element import BaseElement
from usecase.evaluate.elements.activity import Activity
from usecase.evaluate.utils import Element


class SubProcess(BaseElement):
    node: list

    def __init__(self, element: Element):
        super().__init__(element)
        self.node = []


class NormalSubProcess(SubProcess, Activity):
    def __init__(self, element: Element):
        super().__init__(element)


class BPESubProcess(NormalSubProcess):
    def __init__(self, element: Element):
        super().__init__(element)

    def accept(self, t, c, r):
        return t.visit_for_BPESubProcess(self, c, r)


class EventSubProcess(SubProcess):
    def accept(self, t, c, r):
        return t.visit_for_EventSubProcess(self, c, r)


class TransactionSubProcess(NormalSubProcess):
    def accept(self, t, c, r):
        return t.visit_for_TransactionSubProcess(self, c, r)


class CallActivity(NormalSubProcess):
    def accept(self, t, c, r):
        return t.visit_for_CallActivity(self, c, r)
