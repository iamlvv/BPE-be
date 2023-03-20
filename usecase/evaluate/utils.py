from enum import Enum


class Element:
    id: str
    name: str
    incoming: list
    outgoing: list
    incoming_messageflow: list
    outgoing_messageflow: list
    type: str
    className: str
    linkCode: str
    cycleTime: float
    timeDuration: float
    branchingProbabilities: list
    taskType: int
    eventType: int
    isInterrupting: bool
    parentId: str
    boundary: list
    percentage: int

    def __init__(self, **entries):
        self.__dict__.update(entries)


class Context:
    list_gateway: dict
    list_gateway_traveled: dict
    stack_next_gateway: list
    stack_end_loop: list
    in_xor_block: int
    in_loop: int
    in_block: int
    in_transaction_subprocess: list
    number_of_cancel_events: dict

    def __init__(self):
        self.list_gateway = {}
        self.list_gateway_traveled = {}
        self.stack_next_gateway = []
        self.stack_end_loop = []
        self.in_xor_block = 0
        self.in_loop = 0
        self.in_block = 0
        self.in_transaction_subprocess = []
        self.number_of_cancel_events = {}


class Result:
    participant_name: str
    current_cycle_time: float
    number_of_optional_tasks: int
    number_of_total_tasks: int
    flexibility: float
    total_cycle_time_all_loops: float
    logs_cycle_time: list
    logs_quality: list
    logs_flexibility: list
    number_of_handled_exceptions: int
    number_of_unhandled_exceptions: int
    exception_handling: float

    def __init__(self):
        self.participant_name = ""
        self.current_cycle_time = 0.0
        self.number_of_optional_tasks = 0
        self.number_of_total_tasks = 0
        self.flexibility = 0
        self.total_cycle_time_all_loops = 0.0
        self.logs_cycle_time = []
        self.logs_quality = []
        self.logs_flexibility = []
        self.number_of_handled_exceptions = 0
        self.number_of_unhandled_exceptions = 0
        self.exception_handling = 0.0

    def obj_dict(self):
        return self.__dict__


class EventType(Enum):
    START_EVENT = 0
    END_EVENT = 1
    IMPLICIT_THROW_EVENT = 2
    INTERMIDIATE_THROW_EVENT = 3
    INTERMIDIATE_CATCH_EVENT = 4
    BOUNDARY_EVENT = 5


class TaskType(Enum):
    NONE_TASK = 0
    SERVICE_TASK = 1
    MANUAL_TASK = 2
    SCRIPT_TASK = 3
    BUSINESS_TASK = 4
    USER_TASK = 5
