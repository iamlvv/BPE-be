from usecase.evaluate.elements.node import Node
from usecase.evaluate.utils import Element


class Task(Node):
    cycleTime: float

    def __init__(self, element: Element):
        super().__init__(element)
        self.cycleTime = element.cycleTime


class NormalTask(Task):
    taskType: int

    def __init__(self, element: Element):
        super().__init__(element)
        self.taskType = element.taskType

    def accept(self, t, c, r):
        return t.visitForNormalTask(self, c, r)


class MessageTask(Task):
    pass


class SendTask(MessageTask):
    def accept(self, t, c, r):
        return t.visitForSendTask(self, c, r)


class ReceiveTask(MessageTask):
    def accept(self, t, c, r):
        return t.visitForReceiveTask(self, c, r)
