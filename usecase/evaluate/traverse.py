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
        print("Visit task", e.name, e.cycle_time,
              "In xor block", c.in_xor_block)

        r.number_of_total_tasks += 1
        if c.in_xor_block > 0:
            r.number_of_optional_tasks += 1

        total_cycle_time = e.cycle_time

        if not len(e.boundary):
            self.visit(e.next[0], c, r)
            next_time = r.current_cycle_time
            total_cycle_time += next_time
            r.current_cycle_time = total_cycle_time
            return

        if type(e.boundary[0]) is TimerEvent:
            self.visit(e.next[0], c, r)
            next_time = r.current_cycle_time
            self.handle_for_boundary_timer_event(e, c, r, next_time)
            total_cycle_time += r.current_cycle_time
        elif type(e.boundary[0]) is ConditionalEvent:
            self.handle_for_boundary_conditional_event(
                e, e.boundary[0], c, r)

        r.current_cycle_time = total_cycle_time

    def visit_for_SendTask(self, e: SendTask, c: Context, r: Result):
        print(3)

    def visit_for_ReceiveTask(self, e: ReceiveTask, c: Context, r: Result):
        print(7)

    def visit_for_NonEvent(self, e: NonEvent, c: Context, r: Result):
        if e.event_type == EventType.START_EVENT.value:
            print("Visit start event")
            self.visit(e.next[0], c, r)
            return
        elif e.event_type == EventType.END_EVENT.value:
            print("Visit end event")
            r.current_cycle_time = 0
            return

    def visit_for_MessageEvent(self, e: MessageEvent, c: Context, r: Result):
        print("Visit message event")
        if e.event_type == EventType.INTERMIDIATE_THROW_EVENT.value:
            if e.is_start:  # send and start a messsage
                self.visit(e.next[0], c, r)
                next_time = r.current_cycle_time
                new_result = Result()
                self.visit(e.outgoing_messageflow[0], c, new_result)
                message_time = new_result.current_cycle_time
                total_cycle_time = max(next_time, message_time)
                next_node = c.stack_next_message.pop()
                self.visit(next_node, c, r)
                r.current_cycle_time += total_cycle_time
            else:  # receive and stop a message
                r.current_cycle_time = 0
                return
        elif e.event_type == EventType.INTERMIDIATE_CATCH_EVENT.value:
            if e.is_start:  # receive and start a message
                self.visit(e.next[0], c, r)
            else:  # receive and stop a message
                r.current_cycle_time = 0
                c.stack_next_message.append(e.next[0])
        elif e.event_type == EventType.END_EVENT.value:
            if e.code in c.list_event_subprocess:
                # end event triggers a event subprocess
                cycletime_event_subprocess = c.list_event_subprocess[
                    e.code]
                r.current_cycle_time += cycletime_event_subprocess
            else:
                # end event triggers a boundary event
                r.current_cycle_time = 0
            # if e.is_interrupting:
            #     r.current_cycle_time = cycletime_event_subprocess
            # else:
            #     r.current_cycle_time = max(
            #         next_time, cycletime_event_subprocess)
        elif e.event_type == EventType.START_EVENT.value:
            self.visit(e.next[0], c, r)
        elif e.event_type == EventType.BOUNDARY_EVENT.value:
            self.visit(e.next[0], c, r)

    def visit_for_TimerEvent(self, e: TimerEvent, c: Context, r: Result):
        print("Visit timer event")
        if not e.time_duration:
            return
        if e.event_type == EventType.INTERMIDIATE_CATCH_EVENT.value:
            self.visit(e.next[0], c, r)
            r.current_cycle_time += e.time_duration
            return
        elif e.event_type == EventType.BOUNDARY_EVENT.value:
            self.visit(e.next[0], c, r)
            r.current_cycle_time += e.time_duration
            return
        elif e.event_type == EventType.START_EVENT.value and e.is_interrupting:  # same as standard event
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
        print("Visit cancel event")
        # must be attached to transaction subprocess
        if e.event_type == EventType.END_EVENT.value:
            if len(c.in_transaction_subprocess) > 0:
                c.number_of_cancel_events[c.in_transaction_subprocess[-1]
                                          ]["end_event"] += 1
            r.current_cycle_time = 0
            return
        elif e.event_type == EventType.BOUNDARY_EVENT.value:
            self.visit(e.next[0], c, r)
            return

    def visit_for_SignalEvent(self, e: SignalEvent, c: Context, r: Result):
        print()

    def visit_for_MultipleEvent(self, e: MutipleEvent, c: Context, r: Result):
        print()

    def visit_for_CompensationEvent(self, e: CompensationEvent, c: Context, r: Result):
        print()

    def visit_for_ConditionalEvent(self, e: ConditionalEvent, c: Context, r: Result):
        print("Visit conditional event", e.name)
        if e.event_type in [EventType.INTERMIDIATE_THROW_EVENT.value, EventType.START_EVENT.value,
                            EventType.INTERMIDIATE_CATCH_EVENT.value]:
            temp_result = Result()
            self.visit(e.next[0], c, temp_result)
            r.current_cycle_time += e.percentage * temp_result.current_cycle_time
        elif e.event_type == EventType.BOUNDARY_EVENT.value:
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
            self.handle_for_join_gateway(e, c, r)
        elif e.is_split_gateway():
            self.handle_for_split_gateway(e, c, r)
        return

    def visit_for_Lane(self, e: Lane, c: Context, r: Result):
        print("Visit lane", e.name)
        for esp in e.event_sub_process:
            self.visit(esp, c, r)
        if len(e.node) == 0:
            return
        for n in e.node:
            self.visit(n, c, r)

    def visit_for_Participant(self, e: Participant, c: Context, r: Result):
        print("Visit participant", e.name)
        for esp in e.event_sub_process:
            self.visit(esp, c, r)
        for l in e.lane:
            self.visit(l, c, r)
        for n in e.node:
            self.visit(n, c, r)

    def visit_for_EventSubProcess(self, e: EventSubProcess, c: Context, r: Result):
        print("Visit event subprocess")
        # event subprocess must have one and only one start event
        self.visit(e.node[0], c, r)
        c.list_event_subprocess[e.node[0].code] = r.current_cycle_time

    def visit_for_BPESubProcess(self, e: BPESubProcess, c: Context, r: Result):
        print("Visit expanded subprocess")
        self.handle_for_NormalSubProcess(e, c, r)

    def visit_for_TransactionSubProcess(self, e: TransactionSubProcess, c: Context, r: Result):
        print("Visit transaction subprocess")
        c.in_transaction_subprocess.append(e.id)
        c.number_of_cancel_events[e.id] = {
            "end_event": 0,
            "boundary_event": 0
        }
        self.handle_for_NormalSubProcess(e, c, r)
        if c.number_of_cancel_events[e.id]["boundary_event"] > 0 and c.number_of_cancel_events[e.id]["end_event"] > 0:
            r.number_of_handled_exceptions += 1
        elif c.number_of_cancel_events[e.id]["boundary_event"] == 0 and c.number_of_cancel_events[e.id]["end_event"] > 0:
            r.number_of_unhandled_exceptions += 1

    def visit_for_CallActivity(self, e: CallActivity, c: Context, r: Result):
        print("Visit call activity")
        self.handle_for_NormalSubProcess(e, c, r)

    def handle_for_NormalSubProcess(self, e: NormalSubProcess, c: Context, r: Result):
        # traverse all of event sub-processes
        for esp in e.event_sub_process:
            self.visit(esp, c, r)
        # traverse start event of subprocess
        subprocess_time = self.handle_for_inner_SubProcess(e, c, r)
        total_cycle_time = subprocess_time

        if isinstance(e, TransactionSubProcess):
            c.in_transaction_subprocess.remove(e.id)

        self.visit(e.next[0], c, r)
        next_time = r.current_cycle_time

        if not len(e.boundary):
            r.current_cycle_time = total_cycle_time + next_time
            return

        # all boundary timer events must be traversed
        if type(e.boundary[0]) is TimerEvent:
            self.handle_for_boundary_timer_event(e, c, r, next_time)
            total_cycle_time += r.current_cycle_time

        # case subprocess doesn't have any timer event
        if type(e.boundary[0]) is CancelEvent:
            self.handle_for_boundary_cancel_event(e, c, r, next_time)
            total_cycle_time += r.current_cycle_time

        if type(e.boundary[0]) is MessageEvent:
            self.handle_for_boundary_message_event(e, c, r, next_time)
            total_cycle_time += r.current_cycle_time

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
                if type(b) is CancelEvent and b.event_type == EventType.BOUNDARY_EVENT.value:
                    c.number_of_cancel_events[e.id]["boundary_event"] += 1

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
                if n.id not in c.list_gateway_traveled and n.is_split_gateway():
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
        seq_temp_result = Result()

        if interrupt:
            c.in_xor_block += 1

        self.visit(task_from_boundary_event, c, boundary_temp_result)
        self.visit(next_task, c, seq_temp_result)

        if interrupt:
            c.in_xor_block -= 1

        boundary_ct = boundary_temp_result.current_cycle_time
        sequence_ct = seq_temp_result.current_cycle_time

        if interrupt:
            total_cycle_time += percentage * \
                boundary_ct + (1 - percentage) * sequence_ct
        else:
            total_cycle_time += percentage * max(boundary_ct, sequence_ct) + (
                1 - percentage) * sequence_ct
        r.current_cycle_time += total_cycle_time
        r.number_of_optional_tasks += boundary_temp_result.number_of_optional_tasks + \
            seq_temp_result.number_of_optional_tasks
        r.number_of_total_tasks += boundary_temp_result.number_of_total_tasks + \
            seq_temp_result.number_of_total_tasks

    def handle_for_boundary_timer_event(self, e: NormalTask, c: Context, r: Result, next_time: float):
        total_cycle_time = 0.0
        list_boundary_timer_event, is_interrupting = self.handle_for_boundary_SubProcess(
            e, c, r, TimerEvent.__name__)

        if is_interrupting:
            total_cycle_time += max(list_boundary_timer_event)
        else:
            total_cycle_time += max(list_boundary_timer_event, next_time)
        r.current_cycle_time = total_cycle_time

    def handle_for_boundary_cancel_event(self, e: NormalSubProcess, c: Context, r: Result, next_time: float):
        total_cycle_time = 0.0
        list_boundary_cancel_event, _ = self.handle_for_boundary_SubProcess(
            e, c, r, CancelEvent.__name__)

        if len(list_boundary_cancel_event) > 0:
            total_cycle_time += max(list_boundary_cancel_event)

        if len(e.boundary) == 0 and not len(list_boundary_cancel_event):
            total_cycle_time += next_time

        r.current_cycle_time = total_cycle_time

    def handle_for_boundary_message_event(self, e: NormalSubProcess, c: Context, r: Result, next_time: float):
        total_cycle_time = 0.0
        list_boundary_message_event, is_interupting = self.handle_for_boundary_SubProcess(
            e, c, r, MessageEvent.__name__)
        if is_interupting:
            total_cycle_time += max(list_boundary_message_event)
        else:
            total_cycle_time += max(list_boundary_message_event, next_time)
        r.current_cycle_time = total_cycle_time

    def handle_for_join_gateway(self, e: Task, c: Context, r: Result):
        if e.id in c.list_gateway:
            c.list_gateway[e.id] += 1
        else:
            c.list_gateway[e.id] = 1 + \
                self.number_of_gateway_in_nodes(e.previous)

        # Check how many times this join gateway has been visited
        if c.list_gateway[e.id] < len(e.previous):
            r.current_cycle_time = 0
            return

        # Check
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

    def handle_for_split_gateway(self, e: Task, c: Context, r: Result):
        total_cycle_time = 0.0
        next_node = None
        if len(c.stack_end_loop) > 0 and len(e.next) == 2 and c.stack_end_loop[-1] == e:
            print("End loop")
            c.stack_end_loop.pop()
            r.current_cycle_time = 0
            return
        print("Start gateway")

        if isinstance(e, ExclusiveGateway):
            c.in_xor_block += 1

        for i, branch in enumerate(e.next):
            self.visit(branch, c, r)
            print(r.current_cycle_time)
            total_cycle_time += e.branching_probabilities[i] * \
                r.current_cycle_time
            r.current_cycle_time = 0

        if isinstance(e, ExclusiveGateway):
            c.in_xor_block -= 1

        if len(c.stack_next_gateway) > 0:
            next_node = c.stack_next_gateway.pop().next[0]
        else:
            r.current_cycle_time = total_cycle_time
            return
        self.visit(next_node, c, r)
        r.current_cycle_time += total_cycle_time
        return
