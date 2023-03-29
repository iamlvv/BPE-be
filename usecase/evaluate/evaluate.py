from usecase.evaluate.traverse import *
from usecase.evaluate.utils import *


class ProcessDirector:
    map_node_created: dict
    map_element: dict
    linkEventNode: dict

    def __init__(self, map_element):
        self.map_element = map_element
        self.map_node_created = {}
        self.linkEventNode = {}

    def createLinkEventNode(self, instance: LinkEvent, element: Element):
        if instance.linkCode in self.linkEventNode:
            if element.eventType == EventType.INTERMIDIATE_THROW_EVENT.value:
                self.linkEventNode[element.linkCode][0].append(element.id)
            else:
                self.linkEventNode[element.linkCode][1].append(element.id)
        else:
            if element.eventType == EventType.INTERMIDIATE_THROW_EVENT.value:
                self.linkEventNode.update(
                    {element.linkCode: [[element.id], []]})
            else:
                self.linkEventNode.update(
                    {element.linkCode: [[], [element.id]]})

    def handleLinkEvent(self):
        for linkCode in self.linkEventNode:
            throw_nodes = self.get_node_of_ids(self.linkEventNode[linkCode][0])
            catch_node = self.get_node_of_ids(
                self.linkEventNode[linkCode][1])[0]

            for throw_node in throw_nodes:
                next_nodes_of_prev_node = throw_node.previous[0].next
                index_of_link_event = next_nodes_of_prev_node.index(throw_node)
                next_nodes_of_prev_node[index_of_link_event] = catch_node.next[0]

                prev_nodes_of_next_node = catch_node.next[0].previous
                try:
                    index_of_link_event = prev_nodes_of_next_node.index(
                        catch_node)
                    prev_nodes_of_next_node[index_of_link_event] = throw_node.previous[0]
                except:
                    pass

    def create_node(self, element: Element):
        target_class = globals()[element.className]
        instance = target_class(element)

        if isinstance(instance, LinkEvent):
            instance.setAttribute(
                element.linkCode, element.outgoing, element.incoming)
            self.createLinkEventNode(instance, element)

        if isinstance(instance, ConditionalEvent):
            instance.set_percentage(element.percentage)

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
                n.previous = self.get_node_of_ids(e.incoming)
                n.next = self.get_node_of_ids(e.outgoing)
                n.incoming_messageflow = self.get_node_of_ids(
                    e.incoming_messageflow)
                n.outgoing_messageflow = self.get_node_of_ids(
                    e.outgoing_messageflow)
            elif type(n) is Participant:
                collaboration = self.map_node_created[e.parentID]
                collaboration.participants.append(n)
            elif type(n) is Lane:
                participant = self.map_node_created[e.parentID]
                participant.lane.append(n)
            else:
                pass

            if isinstance(n, Event) and n.event_type == EventType.START_EVENT.value:
                lane = self.map_node_created[e.parentID]
                lane.node.append(n)
            if isinstance(n, Activity) and hasattr(e, 'boundary'):
                for b in e.boundary:
                    n.boundary.append(self.map_node_created[b])
            if isinstance(n, SubProcess):
                # get all start event of subprocess
                pass
        self.handleLinkEvent()

        return collaboration


class Collaboration:
    participants: list
    result: list

    def __init__(self, element: Element):
        self.participants = []
        self.result = []


class Evaluate:

    @classmethod
    def evaluate(cls, map_element: dict):
        collaboration = ProcessDirector(map_element).build_graph()
        t = Traverse()
        c = Context()
        for p in collaboration.participants:
            r = Result()
            r.participant_name = p.name
            p.accept(t, c, r)
            if r.number_of_handled_exceptions + r.number_of_unhandled_exceptions > 0:
                r.exception_handling = r.number_of_handled_exceptions / \
                    (r.number_of_handled_exceptions +
                     r.number_of_unhandled_exceptions)
            if r.number_of_total_tasks > 0:
                r.flexibility = r.number_of_optional_tasks / r.number_of_total_tasks
            collaboration.result.append(r)

        return collaboration.result
