from usecase.evaluate.elements.base_element import BaseElement
from usecase.evaluate.elements.activity import Activity
from usecase.evaluate.utils import Element


class SubProcess(BaseElement):
    node: list


class NormalProcess(SubProcess, Activity):
    pass


class ExpandedSubProcess(SubProcess):
    def __init__(self, element: Element):
        super().__init__(element)

    def accept(self, t, c, r):
        return t.visit_for_ExpandedSubProcess(self, c, r)


class EventSubProcess(SubProcess):
    def accept(self, t, c, r):
        return t.visit_for_EventSubProcess(self, c, r)


class TransactionSubProcess(SubProcess):
    def accept(self, t, c, r):
        return t.visit_for_TransactionSubProcess(self, c, r)


class CollapsedSubProcess(SubProcess):
    def accept(self, t, c, r):
        return t.visit_for_CollapsedSubProcess(self, c, r)


class CallActivity(SubProcess):
    def accept(self, t, c, r):
        return t.visit_for_CallActivity(self, c, r)
