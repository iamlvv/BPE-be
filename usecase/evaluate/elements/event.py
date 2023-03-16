from usecase.evaluate.elements.node import Node
from usecase.evaluate.utils import Element, EventType


class Event(Node):
    event_type: EventType
    is_interrupting: bool

    def __init__(self, element: Element):
        super().__init__(element)
        self.event_type = element.eventType
        self.is_interrupting = element.isInterrupting


class NonEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_NonEvent(self, c, r)


class MessageEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_MessageEvent(self, c, r)


class TimerEvent(Event):
    time_duration: float

    def __init__(self, element: Element):
        super().__init__(element)
        self.time_duration = element.timeDuration

    def accept(self, t, c, r):
        return t.visit_for_TimerEvent(self, c, r)


class ErrorEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_ErrorEvent(self, c, r)


class EscalationEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_EscalationEvent(self, c, r)


class CancelEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_CancelEvent(self, c, r)


class SignalEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_SignalEvent(self, c, r)


class MutipleEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_MultipleEvent(self, c, r)


class CompensationEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_CompensationEvent(self, c, r)


class ConditionalEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_ConditionalEvent(self, c, r)


class LinkEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_LinkEvent(self, c, r)


class TerminateEvent(Event):
    def accept(self, t, c, r):
        return t.visit_for_TerminateEvent(self, c, r)
