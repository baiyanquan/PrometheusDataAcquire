import logging

from utils.SockConfig import Config
from utils.utils import Utils
from controller.prometheus.PerformanceDataPicker import PerformanceDataPicker
from controller.prometheus.PerformanceDataWriter import PerformanceDataWriter


def main():
    START_STR = "2019-10-22 18:00:00"
    END_STR = "2019-10-23 14:00:00"
    RESOLUTION = Config.PROMETHEUS_RESOLUTION

    end_time = Utils.datetime_timestamp(END_STR)
    start_time = Utils.datetime_timestamp(START_STR)

    headers, csvsets = PerformanceDataPicker.query_multi_entity_metric_values(queryconfiglist=Config.QUERY_CONFIGS_HW,
                                                                              resolution=Config.PROMETHEUS_RESOLUTION,
                                                                              start_time=start_time,
                                                                              end_time=end_time)

    PerformanceDataWriter.write2csv_merged(filename='data/sock-results-HW_10-23.csv',
                                           metricsnameset=headers, datasets=csvsets)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
