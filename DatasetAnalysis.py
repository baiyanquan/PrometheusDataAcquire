import logging
import pandas as pd
import cProfile

from controller.dataset.CausalityAnalysis import CausalityAnalysis
from controller.dataset.SingleSeriesProcessor import SingleSeriesProcessor
from controller.dataset.DataFrameProcessor import DataFrameProcessor
from controller.graph.GraphBuilder import GraphBuilder
from controller.graph.GraphSearcher import *
from controller.graph.GraphVisualizer import GraphVisualizer

def main():
    start_analysis()

def start_analysis():
    datafile = "data/sock-results-HW_6-20-['service'].csv"
    window_size = 20
    p_threshold = 0.01

    filename = "sock-results-HW_6-20-experiment"
    #filter_groups = [["service"]]
    filter_groups = [["qps", "success_orders"], ["carts/"]]
    #filter_groups = [["service"], ["front-end"], ["carts"], ["container/carts", "192.168.199.31"]]
    #filter_groups = [["service", "192.168.199.35"]]
    #filter_groups = [["service"], ["front-end"], ["carts"], ["orders"], ["catalogue"], ["user"], ["payment"], ["shipping"]]
    #filter_groups = [["container/carts", "192.168.199.31"], ["container/orders", "192.168.199.32"],
                     #["container/user", "192.168.199.32"],
                     #["container/catalogue", "192.168.199.33"],
                     #["container/shipping", "192.168.199.33"],
                     #["container/front-end", "192.168.199.34"], ["container/payment", "192.168.199.35"]]

    # filter_groups = [["service"],
    #                  ["front-end/"], ["carts/"], ["orders/"], ["catalogue/"], ["user/"], ["payment/"], ["shipping/"],
    #                  ["container/carts"], ["container/orders"], ["container/catalogue"], ["container/user"],
    #                  ["container/carts/", "192.168.199.31"], ["container/orders/", "192.168.199.32"],
    #                  ["container/user/", "192.168.199.32"],
    #                  ["container/catalogue/", "192.168.199.33"],
    #                  ["container/shipping/", "192.168.199.33"],
    #                  ["container/front-end/", "192.168.199.34"], ["container/payment/", "192.168.199.35"]
    #                  ]
    data = pd.read_csv("data/%s.csv" % filename)

    #data = DataFrameProcessor.getPartialDataframe(data, end=0.025)
    #data = DataFrameProcessor.getPartialDataframe(data, front=0.0125 ,end=0.025)

    data = data.fillna("null")

    causality_instance = CausalityAnalysis()

    causality_instance.causalInit()

    node_list = []
    edge_list = []
    for filter_list in filter_groups:
        sub_data = DataFrameProcessor.filter_columns(data, filter_list)
        sub_file_name = "%s-%s.csv" % (filename, filter_list)
        sub_file_name = sub_file_name.replace("/", "-")
        sub_file_name = "data/%s" % sub_file_name
        sub_data.to_csv(sub_file_name, index=False)

        nodes, edges = causality_instance.generateCausalityGraph(sub_file_name, "fisherz", "Pc")
        node_list.extend(nodes)
        edge_list.extend(edges)

    causality_instance.causalDest()

    print(node_list)

    data = pd.read_csv("data/%s.csv" % filename)
    data = data.fillna(0)

    for edge in edge_list:
        column1 = data[edge.node1_name]
        column2 = data[edge.node2_name]

        #print(SingleSeriesProcessor.calculate_perason(column1.values,column2.values))

        s1 = SingleSeriesProcessor.get_partial_series(column1.values, .5)
        s2 = SingleSeriesProcessor.get_partial_series(column2.values, .5)

        e_s1, e_s2, cov = getChangeCorrelation(s1, s2, window_size, p_threshold)

        edge.weight = cov

        edge.print()

    edge_list = GraphBuilder.clean_edges(edge_list)
    graph = GraphBuilder.build_graph_dict(edge_list)
    GraphVisualizer.drawCausalityGraph(edge_list)

    #routes = list(GraphSearcher.traverse(graph, "service/front-end/qps(2xx)", stack))
    routes, search_result = GraphSearcher.search_source(graph, "service/orders/success_orders")

    for route in routes:
        print(GraphSearcher.path_to_stirng(route, graph, with_weight=False))

    GraphVisualizer.drawRootCauseGraph(search_result, graph)

def getChangeCorrelation(s1, s2, window_size, p_threshold):

    e_s1 = getChangeEventSeries(s1, window_size, p_threshold)
    e_s2 = getChangeEventSeries(s2, window_size, p_threshold)

    cor = SingleSeriesProcessor.calculate_perason(e_s1, e_s2)

    return e_s1, e_s2, cor

def getChangeEventSeries(s, window_size, p_threshold):

    # = SingleSeriesProcessor.get_ewma(s, window_size)

    #s = SingleSeriesProcessor.exponential_smoothing(0.7, s)

    result = SingleSeriesProcessor.create_value_change_series(s, window_size, p_threshold, True)

    return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()


