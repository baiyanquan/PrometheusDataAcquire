class GraphBuilder:

    def __init__(self):
        pass

    @staticmethod
    def build_graph_dict(edgeList):
        graph = {}

        for edge in edgeList:
            if edge.node1_end == 0:
                GraphBuilder.add_edge(graph, edge.node2_name, edge.node1_name, edge.weight)
            if edge.node2_end == 0:
                GraphBuilder.add_edge(graph, edge.node1_name, edge.node2_name, edge.weight)
        return graph

    @staticmethod
    def add_edge(graph, from_node, to_node, weight):
        if from_node not in graph.keys():
            graph[from_node] = {}
        graph[from_node][to_node] = weight

    @staticmethod
    def clean_edges(edge_list):

        cleaned_list = []
        graph = {}
        for edge in edge_list:
            node1 = edge.node1_name
            node2 = edge.node2_name
            if node1 not in graph.keys():
                graph[node1] = {}
            if node2 not in graph.keys():
                graph[node2] = {}

            if node2 in graph[node1].keys():
                print("exists %s->%s" % (node1, node2))
            elif node1 in graph[node2].keys():
                print("exists reverse %s<-%s" % (node1, node2))
                rev_edge = graph[node2][node1]
                rev_edge.node2_end = 0
            else:
                print("add edge %s->%s" % (node1, node2))
                cleaned_list.append(edge)
                graph[node1][node2] = edge

        return cleaned_list


class Edge:
    def __init__(self):
        self.weight = 0

    def print(self):
        print(
             "%s %d %d %s %f" % (self.node1_name, self.node1_end, self.node2_end, self.node2_name, self.weight))