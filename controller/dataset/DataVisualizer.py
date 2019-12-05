from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np

class DataVisualizer(object):

    def __init__(self):
        pass

    @staticmethod
    def show_single_series(array, label):
        plt.plot(array, label=label)
        plt.legend(loc='lower right')
        plt.show()

    @staticmethod
    def show_predicted_data(series, prediction):
        point = len(series)
        id = range(0, point)
        id_2 = range(point, (point + len(prediction)))
        plt.plot(id, series, color='blue', label="origin_value")
        plt.plot(id_2, prediction, color='red', label="prediction_value")
        plt.legend(loc='lower right')
        plt.show()

    @staticmethod
    def show_markpoints(series, labels):
        plt.plot(series)

        positive_points_x = []
        positive_points_y = []

        negative_points_x = []
        negative_points_y = []

        for i in range(len(labels)):
            if labels[i] == 1:
                positive_points_x.append(i)
                positive_points_y.append(series[i])
            if labels[i] == -1:
                negative_points_x.append(i)
                negative_points_y.append(series[i])

        plt.scatter(positive_points_x, positive_points_y, c='green', marker='o', s=100)
        plt.scatter(negative_points_x, negative_points_y, c='red', marker='o', s=100)

    @staticmethod
    def plotLine(df, x_name):
        valid_markers = ([item[0] for item in mpl.markers.MarkerStyle.markers.items() if
                          item[1] is not 'nothing' and not item[1].startswith('tick') and not item[1].startswith(
                              'caret')])

        # valid_markers = mpl.markers.MarkerStyle.filled_markers

        markers = np.random.choice(valid_markers, df.shape[1], replace=False)

        ax = df.plot(x=x_name, ms=10)

        for i, line in enumerate(ax.get_lines()):
            line.set_marker(markers[i])

        # adding legend
        # ax.legend(ax.get_lines(), data.columns, loc='best')

    @staticmethod
    def plotBars(df, x_name, label, figsize=(10,4)):
        ax = df.plot.bar(x=x_name, figsize=figsize)

        ax.set_ylabel(label)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

