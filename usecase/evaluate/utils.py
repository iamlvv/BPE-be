from enum import Enum


class Element:
    id: str
    name: str
    incoming: list
    outgoing: list
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

    def __init__(self):
        self.list_gateway = {}
        self.list_gateway_traveled = {}
        self.stack_next_gateway = []
        self.stack_end_loop = []
        self.in_xor_block = 0
        self.in_loop = 0
        self.in_block = 0


class Result:
    participant_name: str
    current_cycle_time: float
    number_of_optional_tasks: int
    number_of_total_tasks: int
    total_cycle_time_all_loops: float
    logs_cycle_time: list
    logs_quality: list
    logs_flexibility: list

    def __init__(self):
        self.participant_name = ""
        self.current_cycle_time = 0.0
        self.number_of_optional_tasks = 0
        self.number_of_total_tasks = 0
        self.total_cycle_time_all_loops = 0.0
        self.logs_cycle_time = []
        self.logs_quality = []
        self.logs_flexibility = []

    def obj_dict(self):
        return self.__dict__


class EventType(Enum):
    STARTEVENT = 0
    ENDEVENT = 1
    IMPLICITTHROWEVENT = 2
    INTERMIDIATETHROWEVENT = 3
    INTERMIDIATECATCHEVENT = 4
    BOUNDARYEVENT = 5


class TaskType(Enum):
    NONETASK = 0
    SERVICETASK = 1
    MANUALTASK = 2
    SCRIPTTASK = 3
    BUSINESSTASK = 4
    USERTASK = 5
