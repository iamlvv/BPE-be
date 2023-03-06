from usecase.evaluate.elements.node import Node
from usecase.evaluate.utils import Element


class Task(Node):
    cycle_time: float

    def __init__(self, element: Element):
        super().__init__(element)
        self.cycle_time = element.cycleTime


class NormalTask(Task):
    task_type: int

    def __init__(self, element: Element):
        super().__init__(element)
        self.task_type = element.taskType

    def accept(self, t, c, r):
        return t.visit_for_NormalTask(self, c, r)


class MessageTask(Task):
    pass


class SendTask(MessageTask):
    def accept(self, t, c, r):
        return t.visit_for_SendTask(self, c, r)


class ReceiveTask(MessageTask):
    def accept(self, t, c, r):
        return t.visit_for_ReceiveTask(self, c, r)
