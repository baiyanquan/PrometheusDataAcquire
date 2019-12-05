import logging
import pandas as pd
from matplotlib import pyplot as plt

from controller.dataset.DataFrameProcessor import DataFrameProcessor
from controller.dataset.SingleSeriesProcessor import SingleSeriesProcessor
from controller.dataset.DataVisualizer import DataVisualizer

def main():
    #buildChangeData()
    plotChangePoints()

def buildChangeData():
    #parameters
    filter_words = ["qps", "CPU"]
    window_sizes = [10, 20, 50, 100]
    p_threshold = 0.05
    null_value = -1

    filename = "sock-results-HW_6-20"

    #read dataset
    data = pd.read_csv("data/%s.csv" % filename)

    #filter data with column names
    data = DataFrameProcessor.filter_columns(data, filter_words)
    #data = data.fillna(null_value);

    for window_size in window_sizes:
        print("Analysing Changes on window size: %d" % (window_size))
        result = DataFrameProcessor.create_value_change_dataset(data, window_size, p_threshold)
        result.to_csv("data/%s-%s-%d-%f.csv" % (filename, filter_words, window_size, p_threshold), index=False)

def plotChangePoints():
    window_size = 20
    p_threshold = 0.01

    filename = "sock-results-HW_6-20"
    data = pd.read_csv("data/%s.csv" % filename)

    data = data.fillna(0)

    col_name1 = "container/orders/FS Reads Bytes"
    col_name2 = "service/orders/qps(2xx)"

    #column = data["service/front-end/latency"]
    column = data[col_name1]
    #column = data["service/orders/latency"]
    column2 = data["service/orders/qps(2xx)"]

    #plt.figure(num='fig 1', figsize=(10, 3), dpi=75, facecolor='#FFFFFF', edgecolor='#0000FF')

    s1 = column.values
    s2 = column2.values

    s1 = SingleSeriesProcessor.get_partial_series(s1, front_percentage=.75)
    s2 = SingleSeriesProcessor.get_partial_series(s2, front_percentage=.75)

    e_s1, e_s2, cov = getChangeCorrelation(s1, s2, window_size, p_threshold)

    print(cov)

    plt.title(col_name1)

    DataVisualizer.show_markpoints(s1, e_s1)

    plt.show()

    plt.title(col_name2)

    DataVisualizer.show_markpoints(s2, e_s2)

    plt.show()

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