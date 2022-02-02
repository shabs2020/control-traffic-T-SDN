
import networkx as nx
# import json
# #Check for continuity
# list1 = [[2, 3, 1],[5,6,8], [6, 8]]
# list2 = [6, 8]
#
# check_continuity = True
#
# def _check_continuity (list1, list2):
#     for li in list1:
#         if all(x in li for x in list2):
#             check_continuity = True
#             continue
#         else:
#             check_continuity = False
#             break
#     return check_continuity
#
#
#
#
#
# print("ChecklistItem {}".format(_check_continuity(list1, list2)))
#
#
# with open(
#         "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Nodes_Germany_17.json") as node_file:
#     nodes = json.load(node_file)
# with open(
#         "/home/shabnam/Documents/PHD_SurveyofPapers/ControlPlaneDesign_Proposedtopic/TrafficModelling/PhyNWInfo-master/Germany/Links_Germany_17.json") as edge_file:
#     edges = json.load(edge_file)
class ObjectWithEvents(object):
    callbacks = None

    def on(self, event_name, callback):
        if self.callbacks is None:
            self.callbacks = {}

        if event_name not in self.callbacks:
            self.callbacks[event_name] = [callback]
        else:
            self.callbacks[event_name].append(callback)

    def trigger(self, event_name):
        if self.callbacks is not None and event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(self)

class MyClass(ObjectWithEvents):
    def __init__(self, contents):
        self.contents = contents

    def __str__(self):
        return "MyClass containing " + repr(self.contents)

def echo(value): # because "print" isn't a function...
    print(value)

o = MyClass("hello world")
o.on("example_event", echo)
o.on("example_event", echo)
o.trigger("example_event")

