from enum import Enum


class Element:
    id: str
    name: str
    incoming: list
    outgoing: list
    type: str
    className: str
    cycleTime: float
    branchingProbabilities: list
    taskType: int
    eventType: int
    parentID: str

    def __init__(self, **entries):
        self.__dict__.update(entries)


class Context:
    listGateway: dict
    listGatewayTraveled: dict
    stackNextGateway: list
    stackEndLoop: list
    inXorBlock: int
    inLoop: int
    inBlock: int

    def __init__(self):
        self.listGateway = {}
        self.listGatewayTraveled = {}
        self.stackNextGateway = []
        self.stackEndLoop = []
        self.inXorBlock = 0
        self.inLoop = 0
        self.inBlock = 0


class Result:
    currentCycleTime: float
    numberOfOptionalTasks: int
    numberOfTotalTasks: int
    totalCycleTimeAllLoops: float
    logsCycleTime: list
    logsQuality: list
    logsFlexibility: list

    def __init__(self):
        self.currentCycleTime = 0.0
        self.numberOfOptionalTasks = 0
        self.numberOfTotalTasks = 0
        self.totalCycleTimeAllLoops = 0.0
        self.logsCycleTime = []
        self.logsQuality = []
        self.logsFlexibility = []


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
