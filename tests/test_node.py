from crystaline.net.node import Node

IP = '0.0.0.0'

if __name__ == '__main__':
    my_node = Node(IP)
    my_node.start()