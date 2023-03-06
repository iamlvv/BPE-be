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
        self.create_node_list()
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
        collaboration = ProcessDirector(map_element).build_graph()
        t = Traverse()
        c = Context()
        for p in collaboration.participants:
            r = Result()
            r.participant_name = p.name
            p.accept(t, c, r)
            print(r.current_cycle_time)
            collaboration.result.append(r)

        return collaboration.result
