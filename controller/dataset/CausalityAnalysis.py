import jpype
import os
import logging
import json

from controller.graph.GraphBuilder import Edge

class CausalityAnalysis:

    def __init__(self):
        pass

    def causalInit(self):
        jarpath = os.path.join(os.path.abspath('.'), 'lib\\test-tetrad.jar')
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (jarpath))
        jdClass = jpype.JClass("edu.tongji.xlab.causality.CausalSearch")
        self.instance = jdClass()

    def generateCausalityGraph(self, datafile, indtext, algorithm, alpha=0.05):
        causality_graph_string = self.instance.searchDataset(datafile, indtext, "json", algorithm, alpha)
        causality_graph = json.loads(causality_graph_string)
        node_list = []
        for node in causality_graph["nodes"]:
            node_list.append(node["name"])

        edge_list = []
        for edge in causality_graph["edgesSet"]:
            edge_item = Edge()
            edge_item.node1_name = edge["node1"]["name"]
            edge_item.node1_end = edge["endpoint1"]["ordinal"]
            edge_item.node2_name = edge["node2"]["name"]
            edge_item.node2_end = edge["endpoint2"]["ordinal"]
            # print(
            #     "%s %d %d %s" % (edge_item.node1_name, edge_item.node1_end, edge_item.node2_end, edge_item.node2_name))
            edge_list.append(edge_item)

        return node_list, edge_list

    def causalDest(self):
        jpype.shutdownJVM()


