from DatasetAnalysis import start_analysis
from controller.dataset.DataVisualizer import DataVisualizer

import logging
import psutil
import time
import multiprocessing as mp

def main():
    start_analysis()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    worker_process = mp.Process(target=main)
    worker_process.start()

    p = psutil.Process(worker_process.pid)

    cpu_percents = []
    while worker_process.is_alive():
        try:
            cpu_percent = p.cpu_percent(interval=0.1)
            cpu_percents.append(cpu_percent)
            time.sleep(0.1)
        except psutil.NoSuchProcess:
            break

    worker_process.join()
    print(cpu_percents)
    DataVisualizer.show_single_series(cpu_percents, "cpu percent")
