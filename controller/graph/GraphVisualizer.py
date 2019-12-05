import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
import pygraphviz as pgv
from graphviz import *

class GraphVisualizer():

    def __init__(self):
        pass

    @staticmethod
    def drawGraph():
        G = nx.Graph()
        #G = pgv.AGraph()

        G.add_node("test")
        G.add_edge(2,3)
        print("输出全部节点：{}".format(G.nodes()))
        print("输出全部边：{}".format(G.edges()))
        print("输出全部边的数量：{}".format(G.number_of_edges()))

        write_dot(G, "test.dot")
        pos = graphviz_layout(G)
        nx.draw(G, pos, with_labels=True)

        plt.show()


    @staticmethod
    def drawDiGraph():
        G = nx.DiGraph()
        G.add_node(1)
        G.add_node(2)
        G.add_nodes_from([3, 4, 5, 6])
        G.add_cycle([1, 2, 3, 4])
        G.add_edge(1, 3)
        G.add_edges_from([(3, 5), (3, 6), (6, 7)])
        print("输出全部节点：{}".format(G.nodes()))
        print("输出全部边：{}".format(G.edges()))
        print("输出全部边的数量：{}".format(G.number_of_edges()))
        pos = graphviz_layout(G, prog='dot')
        nx.draw(G, pos, with_labels=True)
        #nx.draw(G, with_labels=True)
        plt.show()

    @staticmethod
    def testGraphviz():
        g = Digraph('测试图片')
        g.node(name='a',color='red')
        g.node(name='b',color='blue')
        g.edge('a','b',color='green')
        g.view()

    @staticmethod
    def drawRootCauseGraph(search_result, graph_dict, drawer='graphviz'):
        if drawer == 'graphviz':
            GraphVisualizer.drawRootCauseGraph_graphviz(search_result, graph_dict)
        elif drawer == 'networkx':
            GraphVisualizer.drawRootCauseGraph_networkx(search_result, graph_dict)

    @staticmethod
    def drawRootCauseGraph_networkx(search_result, graph_dict):
        G = nx.DiGraph()
        G.add_node(search_result.node)
        GraphVisualizer.buildNode_networkx(search_result, G)

        pos = nx.shell_layout(G)
        nx.draw(G, pos, with_labels=True)
        plt.savefig('test_pygraphviz.png', bbox_inches='tight')
        plt.show()

    @staticmethod
    def buildNode_networkx(node, G):
        for sub_node in node.children:
            G.add_node(sub_node.node)
            G.add_edge(sub_node.node, node.node)
            GraphVisualizer.buildNode_networkx(sub_node, G)

    @staticmethod
    def drawRootCauseGraph_graphviz(search_result, graph_dict):
        G = Digraph('causality chain')
        #G.engine = "sfdp"
        G.attr(fontsize='40')
        node_name = GraphVisualizer.transformNodeName(search_result.node)
        #G.node(name=node_name, color='red')
        GraphVisualizer.drawCausalityNode_graphviz(G, node_name)
        GraphVisualizer.buildNode_graphviz(search_result, G, graph_dict)

        G.view()

    @staticmethod
    def buildNode_graphviz(node, G, graph_dict):
        for sub_node in node.children:
            node_name = GraphVisualizer.transformNodeName(node.node)
            sub_node_name = GraphVisualizer.transformNodeName(sub_node.node)
            #G.node(name=sub_node_name, color='blue')
            GraphVisualizer.drawCausalityNode_graphviz(G, sub_node_name)

            #check whether there is already an edge in graph
            tail_name = G._quote_edge(sub_node_name)
            head_name = G._quote_edge(node_name)

            #print(G.body)
            weight = graph_dict[node_name][sub_node_name]
            weight_label = "%f" % weight

            if (G._edge % (tail_name, head_name, (' [label=%s]'% weight_label))) not in G.body:
                G.edge(sub_node_name, node_name, label=weight_label)

            GraphVisualizer.buildNode_graphviz(sub_node, G, graph_dict)

    @staticmethod
    def drawCausalityGraph(edgelist):
        G = Digraph("causality graph")

        G.attr('edge', color='red:black')
        G.attr(fontsize='40')

        for edge in edgelist:

            name1 = GraphVisualizer.transformNodeName(edge.node1_name)
            name2 = GraphVisualizer.transformNodeName(edge.node2_name)

            GraphVisualizer.drawCausalityNode_graphviz(G, name1)
            GraphVisualizer.drawCausalityNode_graphviz(G, name2)

            if edge.node1_end == 0 and edge.node2_end == 0:
                G.edge(name1, name2, color='black', arrowhead="none")
            elif edge.node1_end == 0 and edge.node2_end == 1:
                G.edge(name1, name2, color='black')
            elif edge.node1_end == 1 and edge.node2_end == 0:
                G.edge(name2, name1, color='black')

        G.view()

    @staticmethod
    def transformNodeName(node_name):
        if ":" in node_name:
            name = node_name.replace(":", "-")
        else:
            name = node_name
        return name

    @staticmethod
    def drawCausalityNode_graphviz(G, node_name):
        if "service" in node_name:
            G.node(node_name, color="blue")
        if "container" in node_name:
            G.node(node_name, color="red")
        if "node" in node_name:
            G.node(node_name, color="green")
        else:
            G.node(node_name)
