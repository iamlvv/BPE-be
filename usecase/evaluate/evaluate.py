from usecase.evaluate.traverse import *
from usecase.evaluate.utils import *


class ProcessDirector:
    map_node_created: dict
    map_element: dict

    def __init__(self, map_element):
        self.map_element = map_element
        self.map_node_created = {}

    def create_node(self, element: Element):
        target_class = globals()[element.className]
        instance = target_class(element)
        self.map_node_created[element.id] = instance

    def create_node_list(self):
        for id in self.map_element:
            self.map_element[id] = Element(**self.map_element[id])
            self.create_node(self.map_element[id])

    def get_node_of_ids(self, ids: list):
        result = []
        for id in ids:
            result.append(self.map_node_created[id])
        return result

    def build_graph(self):
        collaboration = None
        for e in self.map_element.values():
            n = self.map_node_created[e.id]
            if isinstance(n, Node):
                if isinstance(n, Event) and n.event_type == EventType.STARTEVENT.value:
                    lane = self.map_node_created[e.parentID]
                    lane.node.append(n)
                n.previous = self.get_node_of_ids(e.incoming)
                n.next = self.get_node_of_ids(e.outgoing)
            elif type(n) is Participant:
                collaboration = self.map_node_created[e.parentID]
                collaboration.participants.append(n)
            elif type(n) is Lane:
                participant = self.map_node_created[e.parentID]
                participant.lane.append(n)
            else:
                pass
        return collaboration


class Collaboration:
    participants: list
    result: list

    def __init__(self, element: Element):
        self.participants = []
        self.result = []


class Evaluate:

    def evaluate(self, map_element: dict):
        # collaboration = Collaboration()
        p = ProcessDirector(map_element)
        p.create_node_list()
        collaboration = p.build_graph()
        t = Traverse()
        c = Context()
        for p in collaboration.participants:
            r = Result()
            p.accept(t, c, r)
            print(r.current_cycle_time)
            collaboration.result.append(r)

        return collaboration.result


j = """
{
    "Id_a77e9019-520a-40b3-84aa-9140b31260d7": {
        "id": "Id_a77e9019-520a-40b3-84aa-9140b31260d7",
        "name": "Process 1",
        "className": "Participant"
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
