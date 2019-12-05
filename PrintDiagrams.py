import pandas as pd
from matplotlib import pyplot as plt
from controller.dataset.DataVisualizer import DataVisualizer
from controller.dataset.DataGenerator import DataGenerator

import logging

#@profile
def main():
    length_data = pd.read_csv("result-length.csv")



    DataVisualizer.plotLine(length_data, "data length")
    # create valid markers from mpl.markers

    plt.show()



    pr_data = pd.read_csv("precision.csv")

    DataVisualizer.plotBars(pr_data, x_name="Service", label='Precision(\%)')

    plt.show()

    pr_data = pd.read_csv("recall.csv")

    DataVisualizer.plotBars(pr_data, x_name="Service", label='Recall(\%)')

    plt.show()


    print(DataGenerator.generate_random_data(7,9,20))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
