import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from net.node import Node

if __name__ == "__main__":
    node = Node("0.0.0.0")
    node.start()
