from usecase.evaluate.utils import *
from usecase.evaluate.elements.base_element import *
from usecase.evaluate.elements.node import *
from usecase.evaluate.elements.gateway import *
from usecase.evaluate.elements.task import *
from usecase.evaluate.elements.event import *
from usecase.evaluate.elements.participant import *
from usecase.evaluate.elements.sub_process import *


class Traverse:
    def visit(self, e, c: Context, r: Result):
        return e.accept(self, c, r)

    def visitForNormalTask(self, e: NormalTask, c: Context, r: Result):
        totalCycleTime = 0.0
        if e.taskType == TaskType.NONETASK.value:
            print("Visit task", e.name)
            nextNode = self.visit(e.next[0], c, r)
            totalCycleTime += r.currentCycleTime + e.cycleTime
            self.calculateCyclyTimeNextNode(nextNode, c, r)
            totalCycleTime += r.currentCycleTime
            r.currentCycleTime = totalCycleTime
            return None

    def visitForSendTask(self, e: SendTask, c: Context, r: Result):
        print(3)

    def visitForReceiveTask(self, e: ReceiveTask, c: Context, r: Result):
        print(7)

    def visitForNonEvent(self, e: NonEvent, c: Context, r: Result):
        if e.eventType == EventType.STARTEVENT.value:
            print("Visit start event")
            nextNode = self.visit(e.next[0], c, r)
            nextResult = r.currentCycleTime
            totalCycleTime = nextResult
            self.calculateCyclyTimeNextNode(nextNode, c, r)
            totalCycleTime += r.currentCycleTime
            r.currentCycleTime = totalCycleTime
        elif e.eventType == EventType.ENDEVENT.value:
            print("Visit end event")
            return None

    def visitForMessageEvent(self, e: MessageEvent, c: Context, r: Result):
        print()

    def visitForTimerEvent(self, e: TimerEvent, c: Context, r: Result):
        print()

    def visitForErrorEvent(self, e: ErrorEvent, c: Context, r: Result):
        print()

    def visitForEscalationEvent(self, e: EscalationEvent, c: Context, r: Result):
        print()

    def visitForCancelEvent(self, e: CancelEvent, c: Context, r: Result):
        print()

    def visitForSignalEvent(self, e: SignalEvent, c: Context, r: Result):
        print()

    def visitForMultipleEvent(self, e: MutipleEvent, c: Context, r: Result):
        print()

    def visitForCompensationEvent(self, e: CompensationEvent, c: Context, r: Result):
        print()

    def visitForConditionalEvent(self, e: ConditionalEvent, c: Context, r: Result):
        print()

    def visitForLinkEvent(self, e: LinkEvent, c: Context, r: Result):
        print()

    def visitForTerminateEvent(self, e: TerminateEvent, c: Context, r: Result):
        print()

    def visitForParallelGateway(self, e: ParallelGateway, c: Context, r: Result):
        c.listGatewayTraveled[e.id] = e

        if e.isJoinGateway():
            if e.id in c.listGateway:
                c.listGateway[e.id] += 1
            else:
                c.listGateway[e.id] = 1 + \
                    self.numberOfGatewayInNodes(e.previous)
            # check so lan da duyet cua cong join
            if c.listGateway[e.id] < len(e.previous):
                r.currentCycleTime = 0
                return None
            print("End parallel gateway")
            c.stackNextGateway.append(e)
            r.currentCycleTime = 0
            return None
        elif e.isSplitGateway():
            totalCycleTime = 0.0
            nextNode = None
            print("Start parallel gateway")
            for branch in e.next:
                nextN = self.visit(branch, c, r)
                branchCycleTime = r.currentCycleTime
                self.calculateCyclyTimeNextNode(nextN, c, r)
                branchCycleTime += r.currentCycleTime
                if totalCycleTime < branchCycleTime:
                    totalCycleTime = branchCycleTime
            if len(c.stackNextGateway) > 0:
                nextNode = c.stackNextGateway.pop().next[0]
            r.currentCycleTime = totalCycleTime
            return nextNode

        r.currentCycleTime = 0
        return None

    def visitForEventBasedGateway(self, e: EventBasedGateway, c: Context, r: Result):
        print()

    def visitForComplexGateway(self, e: ComplexGateway, c: Context, r: Result):
        print()

    def visitForInclusiveGateway(self, e: InclusiveGateway, c: Context, r: Result):
        print()

    def visitForExclusiveGateway(self, e: ExclusiveGateway, c: Context, r: Result):
        c.listGatewayTraveled[e.id] = e

        if e.isJoinGateway():
            if e.id in c.listGateway:
                c.listGateway[e.id] += 1
            else:
                c.listGateway[e.id] = 1 + \
                    self.numberOfGatewayInNodes(e.previous)
            # check so lan da duyet cua cong join
            if c.listGateway[e.id] < len(e.previous):
                r.currentCycleTime = 0
                return None
            # kiem tra xem day la mot gateway bat dau khoi loop hay khong
            check, pre = self.checkNodeTraveled(e.previous, c)
            if not check:
                print("Start loop")
                return None

            print("End gateway")
            c.stackNextGateway.append(e)
            r.currentCycleTime = 0
            return None

        elif e.isSplitGateway():
            totalCycleTime = 0.0
            nextNode = None
            if len(c.stackEndLoop) > 0 and len(e.next) == 2 and c.stackEndLoop[-1] == e:
                print("End loop")
            print("Start gateway")
            for i, branch in enumerate(e.next):
                nextN = self.visit(branch, c, r)
                branchCycleTime = r.currentCycleTime
                self.calculateCyclyTimeNextNode(nextN, c, r)
                branchCycleTime += r.currentCycleTime
                totalCycleTime += e.branchingProbabilities[i] * branchCycleTime

            if len(c.stackNextGateway) > 0:
                nextNode = c.stackNextGateway.pop().next[0]
            r.currentCycleTime = totalCycleTime
            return nextNode

        r.currentCycleTime = 0
        return None

    def visitForLane(self, e: Lane, c: Context, r: Result):
        print("Visit lane", e.name)
        if len(e.node) == 0:
            return None
        for n in e.node:
            self.visit(n, c, r)

    def visitForPool(self, e: Pool, c: Context, r: Result):
        print("Visit pool", e.name)
        for l in e.lane:
            self.visit(l, c, r)

    def visitForExpandedSubProcess(self, e: ExpandedSubProcess, c: Context, r: Result):
        print()

    def visitForEventSubProcess(self, e: EventSubProcess, c: Context, r: Result):
        print()

    def visitForTransactionSubProcess(self, e: TransactionSubProcess, c: Context, r: Result):
        print()

    def visitForCollapsedSubProcess(self, e: CollapsedSubProcess, c: Context, r: Result):
        print()

    def visitForCallActivity(self, e: CallActivity, c: Context, r: Result):
        print()

    def calculateCyclyTimeNextNode(self, nextNode, c: Context, r: Result):
        timeResult = 0.0
        while nextNode != None:
            nextNextNode = self.visit(nextNode, c, r)
            nextNextResult = r.currentCycleTime
            nextNode = nextNextNode
            timeResult += nextNextResult
        r.currentCycleTime = timeResult

    def numberOfGatewayInNodes(self, node) -> int:
        count = 0
        for i in node:
            if isinstance(i, Gateway):
                count += 1
        return count

    def checkNodeTraveled(self, node, c: Context):
        for n in node:
            if isinstance(n, Gateway):
                if n.id not in c.listGatewayTraveled:
                    return False, n
        return True, None
