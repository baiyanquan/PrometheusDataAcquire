import logging
import datetime
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.SockConfig import Config
from utils.utils import Utils
from controller.prometheus.PerformanceDataPicker import PerformanceDataPicker
from controller.prometheus.PerformanceDataWriter import PerformanceDataWriter


def main():
    curr_time = datetime.datetime.now()
    START_STR = ""
    END_STR = ""
    if curr_time.hour < 10:
        START_STR = str(curr_time.date()) + " 0" + str(curr_time.hour - 1) + ":30:00"
        END_STR = str(curr_time.date()) + " 0" + str(curr_time.hour) + ":00:00"
    elif curr_time.hour == 10:
        START_STR = str(curr_time.date()) + " 0" + str(curr_time.hour - 1) + ":30:00"
        END_STR = str(curr_time.date()) + " " + str(curr_time.hour) + ":00:00"
    else:
        START_STR = str(curr_time.date()) + " " + str(curr_time.hour - 1) + ":30:00"
        END_STR = str(curr_time.date()) + " " + str(curr_time.hour) + ":00:00"

    RESOLUTION = Config.PROMETHEUS_RESOLUTION

    end_time = Utils.datetime_timestamp(END_STR)
    start_time = Utils.datetime_timestamp(START_STR)

    headers, csvsets = PerformanceDataPicker.query_multi_entity_metric_values(queryconfiglist=Config.QUERY_CONFIGS_HW,
                                                                              resolution=Config.PROMETHEUS_RESOLUTION,
                                                                              start_time=start_time,
                                                                              end_time=end_time)
    dirs = "data/" + curr_time.strftime("%Y-%m")
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    target_file = dirs + "/" + START_STR.replace("-", "").replace(":", "").replace(" ", "_") + "_SockShopPerformance.csv"
    PerformanceDataWriter.write2csv_merged(
        filename=target_file,
        metricsnameset=headers, datasets=csvsets)


app = Flask(__name__)


@app.route('/api/v1.0/acquire-data', methods=['GET'])
def acquire_data():
    result = {}
    try:
        main()
        result["message"] = "success"
        return jsonify(result)
    except Exception:
        result["message"] = "failure"
        return jsonify(result)


app.route('/api/v1.0/')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')