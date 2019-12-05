import logging
import pandas as pd

from controller.dataset.DataFrameProcessor import DataFrameProcessor

def main():

    #parameters
    filter_words = ["service"]
    filter_words2 = ["qps"]

    filename = "sock-results-HW_6-20"

    #read dataset
    data = pd.read_csv("data/%s.csv" % filename)

    #filter data with column names
    data = DataFrameProcessor.filter_columns(data, filter_words)

    data = DataFrameProcessor.filter_columns(data, filter_words2)


    data = data.fillna("null")
    data.to_csv("data/%s-%s.csv" % (filename, filter_words), index=False)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()