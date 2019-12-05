import math
import numpy as np
import pandas as pd
from scipy import stats

class SingleSeriesProcessor:

    def __init__(self):
        pass

    @staticmethod
    def spiltSeriesByWindow(series, window_size):
        # print ('start spilting series of: %d with window size: %d' % (len(series), window_size))
        result = np.array_split(series, len(series) // window_size)
        # print ('number of sub arrays: %d'% (len(result)))
        return result

    @staticmethod
    def exponential_smoothing(alpha, s):
        s2 = np.zeros(s.shape)
        s2[0] = s[0]
        for i in range(1, len(s2)):
            s2[i] = alpha * s[i] + (1 - alpha) * s2[i - 1]
        return s2

    @staticmethod
    def exponential_smoothing_3(alpha, s):
        s_single = SingleSeriesProcessor.exponential_smoothing(alpha, s)
        s_double = SingleSeriesProcessor.exponential_smoothing(alpha, s_single)
        s_triple = SingleSeriesProcessor.exponential_smoothing(alpha, s_double)

        a_triple = [0 for i in range(len(s))]
        b_triple = [0 for i in range(len(s))]
        c_triple = [0 for i in range(len(s))]

        for i in range(len(s)):
            a_triple[i] = 3 * s_single[i] - 3 * s_double[i] + s_triple[i]

            b_triple[i] = (alpha / (2 * ((1 - alpha) ** 2))) * (
                    (6 - 5 * alpha) * s_single[i] - 2 * ((5 - 4 * alpha) * s_double[i]) + (4 - 3 * alpha) * s_triple[i])

            c_triple[i] = ((alpha ** 2) / (2 * ((1 - alpha) ** 2))) * (s_single[i] - 2 * s_double[i] + s_triple[i])

        return a_triple, b_triple, c_triple

    @staticmethod
    def predict_value_with_exp_smoothing_3(alpha, s):
        a, b, c = SingleSeriesProcessor.exponential_smoothing_3(alpha, s)
        s_temp = []
        s_temp.append(a[0])
        for i in range(len(a)):
            s_temp.append(a[i] + b[i] + c[i])
        return s_temp

    @staticmethod
    def create_value_change_series(series, window, p_threshold, length_kept=False, record_value=False):

        sub_series = SingleSeriesProcessor.spiltSeriesByWindow(series, window)

        column = []
        for i in range(len(sub_series) - 1):
            if length_kept:
                for c in range(window-1):
                    column.append(0)

            first = sub_series[i]
            second = sub_series[i + 1]
            alpha, p_value = stats.ttest_ind(first, second, equal_var=False, nan_policy='omit')
            # print("alpha %f, p %f" % (alpha, p_value))
            if p_value < p_threshold:
                if record_value:
                    column.append(alpha)
                else:
                    if alpha >= 0:
                        column.append(-1)
                    else:
                        column.append(1)
            else:
                column.append(0)

        return column

    @staticmethod
    def get_partial_series(s, back_percentage=1, front_percentage=0):
        length = len(s)
        return s[int(length*front_percentage):int(length*back_percentage)]

    @staticmethod
    def get_ewma(s, window):
        return pd.DataFrame(s).ewm(span=window).mean().values

    @staticmethod
    def calculate_perason(s1, s2):
        length = len(s1)

        sum1 = sum(s1)
        sum2 = sum(s2)

        sum1_sq = sum([pow(v, 2) for v in s1])
        sum2_sq = sum([pow(v, 2) for v in s2])

        p_sum = sum([s1[i]*s2[i] for i in range(length)])

        num = p_sum - (sum1*sum2/length)

        den = math.sqrt((sum1_sq - pow(sum1, 2)/length)*(sum2_sq - pow(sum2, 2)/length))

        if den == 0:
            return 0
        return num/den

