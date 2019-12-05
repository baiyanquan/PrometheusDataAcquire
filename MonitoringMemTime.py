from DatasetAnalysis import start_analysis

import logging

@profile
def main():
    start_analysis()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()