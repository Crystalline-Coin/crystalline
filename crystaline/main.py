import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from crystaline.net.node import Node

if __name__ == "__main__":
    node = Node('localhost')
    node.start()
