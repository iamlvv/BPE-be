from usecase.evaluate.elements.node import Node
from usecase.evaluate.utils import Element


class Gateway(Node):
    def isSplitGateway(self):
        return len(self.next) > 1

    def isJoinGateway(self):
        return len(self.previous) > 1


class ParallelGateway(Gateway):
    def accept(self, t, c, r):
        return t.visitForParallelGateway(self, c, r)


class EventBasedGateway(Gateway):
    def accept(self, t, c, r):
        return t.visitForEventBasedGateway(self, c, r)


class ComplexGateway(Gateway):
    def accept(self, t, c, r):
        return t.visitForComplexGateway(self, c, r)


class InclusiveGateway(Gateway):
    def accept(self, t, c, r):
        return t.visitForInclusiveGateway(self, c, r)


class ExclusiveGateway(Gateway):
    branchingProbabilities: list

    def __init__(self, element: Element):
        super().__init__(element)
        self.branchingProbabilities = element.branchingProbabilities

    def accept(self, t, c, r):
        return t.visitForExclusiveGateway(self, c, r)
