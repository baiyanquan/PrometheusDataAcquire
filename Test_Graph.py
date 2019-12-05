import logging
from controller.graph.GraphVisualizer import GraphVisualizer

def main():
    #GraphVisualizer.drawGraph()
    #GraphVisualizer.drawDiGraph()
    GraphVisualizer.testGraphviz()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()