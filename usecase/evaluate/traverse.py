from usecase.evaluate.utils import *
from usecase.evaluate.elements.gateway import *
from usecase.evaluate.elements.task import *
from usecase.evaluate.elements.event import *
from usecase.evaluate.elements.participant import *
from usecase.evaluate.elements.sub_process import *


class Traverse:
    def visit(self, e, c: Context, r: Result):
        e.accept(self, c, r)

    def visit_for_NormalTask(self, e: NormalTask, c: Context, r: Result):
        print("Visit task", e.name, e.cycle_time)

        if len(e.boundary) > 0:
            for boundary_event in e.boundary:
                if isinstance(boundary_event, ConditionalEvent):
                    self.handle_for_boundary_conditional_event(e, boundary_event, c, r)
                elif isinstance(boundary_event, TimerEvent):
                    total_cycle_time = self.handle_for_boundary_timer_event(e, c, r)
                    r.current_cycle_time = total_cycle_time
        else:
            self.visit(e.next[0], c, r)
            r.current_cycle_time += e.cycle_time

    def visit_for_SendTask(self, e: SendTask, c: Context, r: Result):
        print(3)

    def visit_for_ReceiveTask(self, e: ReceiveTask, c: Context, r: Result):
        print(7)

    def visit_for_NonEvent(self, e: NonEvent, c: Context, r: Result):
        if e.event_type == EventType.STARTEVENT.value:
            print("Visit start event")
            self.visit(e.next[0], c, r)
            return
        elif e.event_type == EventType.ENDEVENT.value:
            print("Visit end event")
            r.current_cycle_time = 0
            return

    def visit_for_MessageEvent(self, e: MessageEvent, c: Context, r: Result):
        print()

    def visit_for_TimerEvent(self, e: TimerEvent, c: Context, r: Result):
        print("Visit timer event")
        if not e.time_duration:
            return
        if e.event_type == EventType.INTERMIDIATECATCHEVENT.value:
            self.visit(e.next[0], c, r)
            r.current_cycle_time += e.time_duration
            return
        elif e.event_type == EventType.BOUNDARYEVENT.value:
            self.visit(e.next[0], c, r)
            r.current_cycle_time += e.time_duration
            return
        elif e.event_type == EventType.STARTEVENT.value and e.is_interrupting:  # same as standard event
            self.visit(e.next[0], c, r)
            r.current_cycle_time += e.time_duration
            return
        else:  # case start event non-interrupting
            pass

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
        print("Visit conditional event", e.name)
        if e.event_type in [EventType.INTERMIDIATETHROWEVENT.value, EventType.STARTEVENT.value,
                            EventType.INTERMIDIATECATCHEVENT.value]:
            temp_result = Result()
            self.visit(e.next[0], c, temp_result)
            r.current_cycle_time += e.percentage * temp_result.current_cycle_time
            print()
        elif e.event_type == EventType.BOUNDARYEVENT.value:
            pass

    def visit_for_LinkEvent(self, e: LinkEvent, c: Context, r: Result):
        pass

    def visit_for_TerminateEvent(self, e: TerminateEvent, c: Context, r: Result):
        print("Visit terminate event")
        r.current_cycle_time = 0
        return

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
                return
            print("End parallel gateway")
            c.stack_next_gateway.append(e)
            r.current_cycle_time = 0
            return
        elif e.is_split_gateway():
            total_cycle_time = 0.0
            next_node = None
            print("Start parallel gateway")
            for branch in e.next:
                self.visit(branch, c, r)
                branch_cycle_time = r.current_cycle_time
                if total_cycle_time < branch_cycle_time:
                    total_cycle_time = branch_cycle_time
            if len(c.stack_next_gateway) > 0:
                next_node = c.stack_next_gateway.pop().next[0]
            self.visit(next_node, c, r)
            r.current_cycle_time += total_cycle_time
            return

        r.current_cycle_time = 0
        return

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
                return
            # kiem tra xem day la mot gateway bat dau khoi loop hay khong
            check, pre = self.check_exclusive_gateway_traveled(e.previous, c)
            if not check:
                print("Start loop")
                c.stack_end_loop.append(pre)
                self.handle_for_loop(e, pre, c, r)
                return

            print("End gateway")
            c.stack_next_gateway.append(e)
            r.current_cycle_time = 0
            return

        elif e.is_split_gateway():
            total_cycle_time = 0.0
            next_node = None
            if len(c.stack_end_loop) > 0 and len(e.next) == 2 and c.stack_end_loop[-1] == e:
                print("End loop")
                c.stack_end_loop.pop()
                r.current_cycle_time = 0
                return
            print("Start gateway")
            for i, branch in enumerate(e.next):
                self.visit(branch, c, r)
                total_cycle_time += e.branching_probabilities[i] * \
                                    r.current_cycle_time

            if len(c.stack_next_gateway) > 0:
                next_node = c.stack_next_gateway.pop().next[0]
            self.visit(next_node, c, r)
            r.current_cycle_time += total_cycle_time
            return

        r.current_cycle_time = 0
        return

    def visit_for_Lane(self, e: Lane, c: Context, r: Result):
        print("Visit lane", e.name)
        if len(e.node) == 0:
            return
        for n in e.node:
            self.visit(n, c, r)

    def visit_for_Participant(self, e: Participant, c: Context, r: Result):
        print("Visit participant", e.name)
        for l in e.lane:
            self.visit(l, c, r)
        for n in e.node:
            self.visit(n, c, r)

    def visit_for_EventSubProcess(self, e: EventSubProcess, c: Context, r: Result):
        print("Visit expanded subprocess")
        # traverse start event of subprocess
        subprocess_time = 0.0
        # expected subprocess has only one start event
        for se in e.node:
            self.visit(se, c, r)
            subprocess_time += r.current_cycle_time

        r.current_cycle_time = subprocess_time

    def visit_for_BPESubProcess(self, e: BPESubProcess, c: Context, r: Result):
        print("Visit expanded subprocess")
        self.handle_for_NormalSubProcess(e, c, r)

    def visit_for_TransactionSubProcess(self, e: TransactionSubProcess, c: Context, r: Result):
        print("Visit transaction subprocess")
        self.handle_for_NormalSubProcess(e, c, r)

    def visit_for_CallActivity(self, e: CallActivity, c: Context, r: Result):
        print("Visit call activity")
        self.handle_for_NormalSubProcess(e, c, r)

    def handle_for_NormalSubProcess(self, e: NormalSubProcess, c: Context, r: Result):
        # traverse start event of subprocess
        subprocess_time = self.handle_for_inner_SubProcess(e, c, r)
        total_cycle_time = subprocess_time

        # all boundary timer events must be traversed
        list_boundary_timer_event, is_interrupting = self.handle_for_boundary_SubProcess(
            e, c, r, TimerEvent.__name__)

        self.visit(e.next[0], c, r)
        next_time = r.current_cycle_time

        if len(list_boundary_timer_event) > 0:
            # case for timer event
            if is_interrupting:
                total_cycle_time += max(list_boundary_timer_event)
            else:
                total_cycle_time += max(max(list_boundary_timer_event),
                                        next_time)
        else:  # case subprocess doesn't have any timer event
            total_cycle_time += next_time

        r.current_cycle_time = total_cycle_time

    def handle_for_inner_SubProcess(self, e: NormalSubProcess, c: Context, r: Result):
        # return cycle time of subprocess and list of boundary events cycletime
        subprocess_time = 0.0
        # expected subprocess has only one start event
        for se in e.node:
            self.visit(se, c, r)
            subprocess_time += r.current_cycle_time

        return subprocess_time

    def handle_for_boundary_SubProcess(self, e: NormalSubProcess, c: Context, r: Result, class_name: str):
        list_boundary_time = []
        is_interrupting = True

        for b in e.boundary:
            # timer event case take all cycle time of boundary
            if type(b).__name__ == class_name:
                is_interrupting = b.is_interrupting
                self.visit(b, c, r)
                list_boundary_time.append(r.current_cycle_time)

        return list_boundary_time, is_interrupting

    def number_of_gateway_in_nodes(self, node) -> int:
        count = 0
        for i in node:
            if isinstance(i, Gateway):
                count += 1
        return count

    def check_exclusive_gateway_traveled(self, node, c: Context):
        for n in node:
            if type(n) is ExclusiveGateway:
                if n.id not in c.list_gateway_traveled:
                    return False, n
        return True, None

    def handle_for_loop(self, start: ExclusiveGateway, end: ExclusiveGateway, c: Context, r: Result):
        self.visit(start.next[0], c, r)

        reloop = 0.0
        next_node = None
        for i, n in enumerate(end.next):
            if isinstance(n, Gateway) and n == start:
                reloop = end.branching_probabilities[i]
            else:
                next_node = n
        total_cycle_time = r.current_cycle_time / (1 - reloop)
        self.visit(next_node, c, r)
        r.current_cycle_time += total_cycle_time
        return

    def handle_for_boundary_conditional_event(self, e: NormalTask, boundary_event: ConditionalEvent, c: Context,
                                              r: Result):
        interrupt = boundary_event.is_interrupting
        percentage = boundary_event.percentage

        task_from_boundary_event = boundary_event.next[0]
        next_task = e.next[0]

        total_cycle_time = e.cycle_time

        boundary_temp_result = Result()
        self.visit(task_from_boundary_event, c, boundary_temp_result)

        seq_temp_result = Result()
        self.visit(next_task, c, seq_temp_result)

        boundary_ct = boundary_temp_result.current_cycle_time
        sequence_ct = seq_temp_result.current_cycle_time

        if interrupt:
            total_cycle_time += percentage * boundary_ct + (1 - percentage) * sequence_ct
        else:
            total_cycle_time += percentage * max(boundary_ct, sequence_ct) + (
                    1 - percentage) * sequence_ct
        r.current_cycle_time += total_cycle_time

    def handle_for_boundary_timer_event(self, e: NormalTask, c: Context, r: Result):
        task_time = e.cycle_time
        total_cycle_time = task_time
        list_boundary_timer_event, is_interrupting = self.handle_for_boundary_SubProcess(
            e, c, r, TimerEvent.__name__)

        self.visit(e.next[0], c, r)
        next_time = r.current_cycle_time

        if is_interrupting:
            total_cycle_time += max(list_boundary_timer_event)
        else:
            total_cycle_time += max(list_boundary_timer_event, next_time)
        return total_cycle_time
