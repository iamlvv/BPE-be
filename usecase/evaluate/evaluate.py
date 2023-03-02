from usecase.evaluate.traverse import *
from usecase.evaluate.utils import *


class ProcessDirector:
    mapNodeCreated: dict
    mapElement: dict

    def __init__(self, mapElement):
        self.mapElement = mapElement
        self.mapNodeCreated = {}

    def createNode(self, element: Element):
        targetClass = globals()[element.className]
        instance = targetClass(element)
        self.mapNodeCreated[element.id] = instance

    def createNodeList(self):
        for id in self.mapElement:
            self.mapElement[id] = Element(**self.mapElement[id])
            self.createNode(self.mapElement[id])

    def getNodeOfIds(self, ids: list):
        result = []
        for id in ids:
            result.append(self.mapNodeCreated[id])
        return result

    def buildGraph(self):
        startNode = None
        for e in self.mapElement.values():
            n = self.mapNodeCreated[e.id]
            if isinstance(n, Node):
                if isinstance(n, Event) and n.eventType == EventType.STARTEVENT.value:
                    lane = self.mapNodeCreated[e.parentID]
                    lane.node.append(n)
                n.previous = self.getNodeOfIds(e.incoming)
                n.next = self.getNodeOfIds(e.outgoing)
            elif type(n) is Pool:
                startNode = n
            elif type(n) is Lane:
                pool = self.mapNodeCreated[e.parentID]
                pool.lane.append(n)
            else:
                pass
        return startNode


class Process:
    pool: list

    def __init__(self):
        self.pool = []


class Evaluate:
    result: Result

    def __init__(self) -> None:
        self.result = Result()

    def evaluate(self, mapElement: dict):
        p = ProcessDirector(mapElement)
        p.createNodeList()
        startNode = p.buildGraph()
        t = Traverse()
        c = Context()
        startNode.accept(t, c, self.result)


j = """
{
    "Id_a77e9019-520a-40b3-84aa-9140b31260d7": {
        "id": "Id_a77e9019-520a-40b3-84aa-9140b31260d7",
        "name": "Process 1",
        "className": "Pool"
    },
    "Lane_04n071y": {
        "id": "Lane_04n071y",
        "name": "123",
        "className": "Lane",
        "parentID": "Id_a77e9019-520a-40b3-84aa-9140b31260d7"
    },
    "Event_0s5inu0": {
        "id": "Event_0s5inu0",
        "name": "StartEvent",
        "incoming": [],
        "outgoing": [
            "Activity_01i35r5"
        ],
        "type": "event",
        "className": "NonEvent",
        "cycleTime": 0,
        "branchingProbabilities": [],
        "eventType": 0,
        "parentID": "Lane_04n071y"
    },
    "Activity_01i35r5": {
        "id": "Activity_01i35r5",
        "name": "task 1",
        "incoming": [
            "Event_0s5inu0"
        ],
        "outgoing": [
            "gateway1"
        ],
        "type": "task",
        "className": "NormalTask",
        "cycleTime": 2,
        "branchingProbabilities": [],
        "taskType": 0,
        "parentID": "Lane_04n071y"
    },
    "gateway1": {
        "id": "gateway1",
        "name": "gateway 1",
        "incoming": [
            "Activity_01i35r5"
        ],
        "outgoing": [
            "Activity_01i35r6",
            "Activity_01i35r7"
        ],
        "type": "task",
        "className": "ParallelGateway",
        "cycleTime": 0,
        "branchingProbabilities": [],
        "taskType": 0,
        "parentID": "Lane_04n071y"
    },
    "Activity_01i35r6": {
        "id": "Activity_01i35r6",
        "name": "task 2",
        "incoming": [
            "Activity_01i35r5"
        ],
        "outgoing": [
            "gateway2"
        ],
        "type": "task",
        "className": "NormalTask",
        "cycleTime": 5,
        "branchingProbabilities": [],
        "taskType": 0,
        "parentID": "Lane_04n071y"
    },
    "Activity_01i35r7": {
        "id": "Activity_01i35r7",
        "name": "task 3",
        "incoming": [
            "Activity_01i35r5"
        ],
        "outgoing": [
            "gateway2"
        ],
        "type": "task",
        "className": "NormalTask",
        "cycleTime": 4,
        "branchingProbabilities": [],
        "taskType": 0,
        "parentID": "Lane_04n071y"
    },
    "gateway2": {
        "id": "gateway2",
        "name": "gateway 2",
        "incoming": [
            "Activity_01i35r6",
            "Activity_01i35r7"
        ],
        "outgoing": [
            "Event_014clh1"
        ],
        "type": "task",
        "className": "ParallelGateway",
        "cycleTime": 0,
        "branchingProbabilities": [],
        "taskType": 0,
        "parentID": "Lane_04n071y"
    },
    "Event_014clh1": {
        "id": "Event_014clh1",
        "name": "EndEvent",
        "incoming": [
            "gateway2"
        ],
        "outgoing": [],
        "type": "event",
        "className": "NonEvent",
        "cycleTime": 0,
        "branchingProbabilities": [],
        "eventType": 1,
        "parentID": "Lane_04n071y"
    }
}
"""
