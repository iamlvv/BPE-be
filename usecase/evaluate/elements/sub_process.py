from usecase.evaluate.elements.base_element import BaseElement
from usecase.evaluate.elements.node import Node
from usecase.evaluate.utils import Element


class SubProcess(BaseElement):
    node: list
    boundary: list


class NormalProcess(SubProcess, Node):
    pass


class ExpandedSubProcess(SubProcess):
    def __init__(self, element: Element):
        super().__init__()

    def accept(self, t, c, r):
        return t.visitForExpandedSubProcess(self, c, r)


class EventSubProcess(SubProcess):
    def accept(self, t, c, r):
        return t.visitForEventSubProcess(self, c, r)


class TransactionSubProcess(SubProcess):
    def accept(self, t, c, r):
        return t.visitForTransactionSubProcess(self, c, r)


class CollapsedSubProcess(SubProcess):
    def accept(self, t, c, r):
        return t.visitForCollapsedSubProcess(self, c, r)


class CallActivity(SubProcess):
    def accept(self, t, c, r):
        return t.visitForCallActivity(self, c, r)
