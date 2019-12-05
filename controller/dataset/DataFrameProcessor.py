# -*- coding: utf-8 -*
import pandas as pd
from scipy import stats

from controller.dataset.SingleSeriesProcessor import SingleSeriesProcessor

class DataFrameProcessor(object):

    def __init__(self):
        pass

    @staticmethod
    def filter_columns(df, filters):
        indexes = df.columns.values
        # print(indexes)
        filtered_indexes = []
        for filter_word in filters:
            for index in indexes:
                if filter_word in index:
                    if filter_word not in filtered_indexes:
                        filtered_indexes.append(index)
        filtered_df = df[filtered_indexes]
        return filtered_df

    @staticmethod
    def create_value_change_dataset(df, window, p_threshold):
        dataset = pd.DataFrame()

        for index in df.columns.values:
            series = df[index]
            sub_series = SingleSeriesProcessor.spiltSeriesByWindow(series.values, window)

            column = []
            for i in range(len(sub_series) - 1):
                first = sub_series[i]
                second = sub_series[i + 1]
                alpha, p_value = stats.ttest_ind(first, second, equal_var=False, nan_policy='omit')
                # print("alpha %f, p %f" % (alpha, p_value))
                if p_value > p_threshold:
                    # if alpha >= 0:
                    #     column.append(-1)
                    # else:
                    #     column.append(1)
                    column.append(alpha)
                else:
                    column.append(0)

            dataset[index] = column
            return dataset

    @staticmethod
    def getPartialDataframe(df, front=0, end=1):
        length = df.shape[0]
        front_index = int(length * front)
        end_index = int(length * end)
        return df.ix[front_index:end_index]
