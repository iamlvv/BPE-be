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

    def visit_for_NormalTask(self, e: NormalTask, c: Context, r: Result):
        total_cycle_time = 0.0
        if e.task_type == TaskType.NONETASK.value:
            print("Visit task", e.name)
            next_node = self.visit(e.next[0], c, r)
            total_cycle_time += r.current_cycle_time + e.cycle_time
            self.calculate_cycle_time_nextNode(next_node, c, r)
            total_cycle_time += r.current_cycle_time
            r.current_cycle_time = total_cycle_time
            return None

    def visit_for_SendTask(self, e: SendTask, c: Context, r: Result):
        print(3)

    def visit_for_ReceiveTask(self, e: ReceiveTask, c: Context, r: Result):
        print(7)

    def visit_for_NonEvent(self, e: NonEvent, c: Context, r: Result):
        if e.event_type == EventType.STARTEVENT.value:
            print("Visit start event")
            next_node = self.visit(e.next[0], c, r)
            next_result = r.current_cycle_time
            total_cycle_time = next_result
            self.calculate_cycle_time_nextNode(next_node, c, r)
            total_cycle_time += r.current_cycle_time
            r.current_cycle_time = total_cycle_time
        elif e.event_type == EventType.ENDEVENT.value:
            print("Visit end event")
            return None

    def visit_for_MessageEvent(self, e: MessageEvent, c: Context, r: Result):
        print()

    def visit_for_TimerEvent(self, e: TimerEvent, c: Context, r: Result):
        print()

    def visit_for_ErrorEvent(self, e: ErrorEvent, c: Context, r: Result):
        print()

    def visit_for_EscalationEvent(self, e: EscalationEvent, c: Context, r: Result):
        print()

    def visit_for_CancelEvent(self, e: CancelEvent, c: Context, r: Result):
        print()

    def visit_for_SignalEvent(self, e: SignalEvent, c: Context, r: Result):
        print()

    def visit_for_MultipleEvent(self, e: MutipleEvent, c: Context, r: Result):
        print()

    def visit_for_CompensationEvent(self, e: CompensationEvent, c: Context, r: Result):
        print()

    def visit_for_ConditionalEvent(self, e: ConditionalEvent, c: Context, r: Result):
        print()

    def visit_for_LinkEvent(self, e: LinkEvent, c: Context, r: Result):
        print()

    def visit_for_TerminateEvent(self, e: TerminateEvent, c: Context, r: Result):
        print()

    def visit_for_ParallelGateway(self, e: ParallelGateway, c: Context, r: Result):
        c.list_gateway_traveled[e.id] = e

        if e.is_join_gateway():
            if e.id in c.list_gateway:
                c.list_gateway[e.id] += 1
            else:
                c.list_gateway[e.id] = 1 + \
                    self.number_of_gateway_in_nodes(e.previous)
            # check so lan da duyet cua cong join
            if c.list_gateway[e.id] < len(e.previous):
                r.current_cycle_time = 0
                return None
            print("End parallel gateway")
            c.stack_next_gateway.append(e)
            r.current_cycle_time = 0
            return None
        elif e.is_split_gateway():
            total_cycle_time = 0.0
            next_node = None
            print("Start parallel gateway")
            for branch in e.next:
                next_N = self.visit(branch, c, r)
                branch_cycle_time = r.current_cycle_time
                self.calculate_cycle_time_nextNode(next_N, c, r)
                branch_cycle_time += r.current_cycle_time
                if total_cycle_time < branch_cycle_time:
                    total_cycle_time = branch_cycle_time
            if len(c.stack_next_gateway) > 0:
                next_node = c.stack_next_gateway.pop().next[0]
            r.current_cycle_time = total_cycle_time
            return next_node

        r.current_cycle_time = 0
        return None

    def visit_for_EventBasedGateway(self, e: EventBasedGateway, c: Context, r: Result):
        print()

    def visit_for_ComplexGateway(self, e: ComplexGateway, c: Context, r: Result):
        print()

    def visit_for_InclusiveGateway(self, e: InclusiveGateway, c: Context, r: Result):
        print()

    def visit_for_ExclusiveGateway(self, e: ExclusiveGateway, c: Context, r: Result):
        c.list_gateway_traveled[e.id] = e

        if e.is_join_gateway():
            if e.id in c.list_gateway:
                c.list_gateway[e.id] += 1
            else:
                c.list_gateway[e.id] = 1 + \
                    self.number_of_gateway_in_nodes(e.previous)
            # check so lan da duyet cua cong join
            if c.list_gateway[e.id] < len(e.previous):
                r.current_cycle_time = 0
                return None
            # kiem tra xem day la mot gateway bat dau khoi loop hay khong
            check, pre = self.check_node_traveled(e.previous, c)
            if not check:
                print("Start loop")
                return None

            print("End gateway")
            c.stack_next_gateway.append(e)
            r.current_cycle_time = 0
            return None

        elif e.is_split_gateway():
            total_cycle_time = 0.0
            next_node = None
            if len(c.stack_end_loop) > 0 and len(e.next) == 2 and c.stack_end_loop[-1] == e:
                print("End loop")
            print("Start gateway")
            for i, branch in enumerate(e.next):
                nextN = self.visit(branch, c, r)
                branch_cycle_time = r.current_cycle_time
                self.calculate_cycle_time_nextNode(nextN, c, r)
                branch_cycle_time += r.current_cycle_time
                total_cycle_time += e.branching_probabilities[i] * \
                    branch_cycle_time

            if len(c.stack_next_gateway) > 0:
                next_node = c.stack_next_gateway.pop().next[0]
            r.current_cycle_time = total_cycle_time
            return next_node

        r.current_cycle_time = 0
        return None

    def visit_for_Lane(self, e: Lane, c: Context, r: Result):
        print("Visit lane", e.name)
        if len(e.node) == 0:
            return None
        for n in e.node:
            self.visit(n, c, r)

    def visit_for_Pool(self, e: Pool, c: Context, r: Result):
        print("Visit pool", e.name)
        for l in e.lane:
            self.visit(l, c, r)

    def visit_for_ExpandedSubProcess(self, e: ExpandedSubProcess, c: Context, r: Result):
        print()

    def visit_for_EventSubProcess(self, e: EventSubProcess, c: Context, r: Result):
        print()

    def visit_for_TransactionSubProcess(self, e: TransactionSubProcess, c: Context, r: Result):
        print()

    def visit_for_CollapsedSubProcess(self, e: CollapsedSubProcess, c: Context, r: Result):
        print()

    def visit_for_CallActivity(self, e: CallActivity, c: Context, r: Result):
        print()

    def calculate_cycle_time_nextNode(self, next_node, c: Context, r: Result):
        time_result = 0.0
        while next_node != None:
            next_next_node = self.visit(next_node, c, r)
            next_next_result = r.current_cycle_time
            next_node = next_next_node
            time_result += next_next_result
        r.current_cycle_time = time_result

    def number_of_gateway_in_nodes(self, node) -> int:
        count = 0
        for i in node:
            if isinstance(i, Gateway):
                count += 1
        return count

    def check_node_traveled(self, node, c: Context):
        for n in node:
            if isinstance(n, Gateway):
                if n.id not in c.list_gateway_traveled:
                    return False, n
        return True, None
