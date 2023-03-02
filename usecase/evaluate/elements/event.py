from usecase.evaluate.elements.node import Node
from usecase.evaluate.utils import Element, EventType


class Event(Node):
    eventType: EventType

    def __init__(self, element: Element):
        super().__init__(element)
        self.eventType = element.eventType


class NonEvent(Event):
    def accept(self, t, c, r):
        return t.visitForNonEvent(self, c, r)


class MessageEvent(Event):
    def accept(self, t, c, r):
        return t.visitForMessageEvent(self, c, r)


class TimerEvent(Event):
    def accept(self, t, c, r):
        return t.visitForTimerEvent(self, c, r)


class ErrorEvent(Event):
    def accept(self, t, c, r):
        return t.visitForErrorEvent(self, c, r)


class EscalationEvent(Event):
    def accept(self, t, c, r):
        return t.visitForEscalationEvent(self, c, r)


class CancelEvent(Event):
    def accept(self, t, c, r):
        return t.visitForCancelEvent(self, c, r)


class SignalEvent(Event):
    def accept(self, t, c, r):
        return t.visitForSignalEvent(self, c, r)


class MutipleEvent(Event):
    def accept(self, t, c, r):
        return t.visitForMultipleEvent(self, c, r)


class CompensationEvent(Event):
    def accept(self, t, c, r):
        return t.visitForCompensationEvent(self, c, r)


class ConditionalEvent(Event):
    def accept(self, t, c, r):
        return t.visitForConditionalEvent(self, c, r)


class LinkEvent(Event):
    def accept(self, t, c, r):
        return t.visitForLinkEvent(self, c, r)


class TerminateEvent(Event):
    def accept(self, t, c, r):
        return t.visitForTerminateEvent(self, c, r)
