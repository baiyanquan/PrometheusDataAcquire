import logging
import pandas as pd
from matplotlib import pyplot as plt

from controller.dataset.DataVisualizer import DataVisualizer
from controller.dataset.SingleSeriesProcessor import SingleSeriesProcessor

from GreyPrediction import GrayForecast

def main():
    data = pd.read_csv("data/sock-results-HW_6-20.csv")
    data = data.fillna(0)

    column_name = "node/192.168.199.33:9100/CPU Usage"
    column = data[column_name]

    #column.plot()
    #plt.show()

    #DataVisualizer.show_single_series(column.values,"service/carts/qps(2xx)")

    alpha = 0.70

    #gf = GrayForecast(column.values, "service/front-end/qps(2xx)")
    gf = GrayForecast(column.values, column_name)
    #print(gf.level_check())
    gf.forecast(time=4000, forecast_data_len=4000)
    gf.log()
    gf.plot()
    column.plot()

    plt.show()

    #DoExponetialSmooting(column.values, alpha)

    #PredictByHoltWinters(column.values, alpha)

def DoExponetialSmooting(series, alpha):
    results = pd.DataFrame()
    s_single = SingleSeriesProcessor.exponential_smoothing(alpha, series)
    results["single_smoothing"] = s_single
    s_double = SingleSeriesProcessor.exponential_smoothing(alpha, s_single)
    results["double_smoothing"] = s_double
    results.plot()
    plt.show()

def PredictByHoltWinters(series, alpha):
    predict = SingleSeriesProcessor.predict_value_with_exp_smoothing_3(alpha, series)
    DataVisualizer.show_predicted_data(series, predict)
    plt.plot(predict, label="predict")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
