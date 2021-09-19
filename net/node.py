import sys, _thread
from flask import Flask
from flask import request
import requests
import json
from crystaline.blockchain.Blockchain import Blockchain

PROT = "http"
DEFAULT_PORT = 5000
URI_GET_NODES = "/get_nodes"
URI_ADD_NODE = "/add_node"
URI_GET_STATUS = "/get_status"
URI_GET_BLOCK = "/get_block" 

STATUS_RUNNING = 'UP'
STATUS_NOT_RESPONDING = 'DOWN'

IP_PARAM = "dst_ip"
PORT_PARAM = "dst_port"
BLOCK_INDEX_PARAM = 'n'
class Node:
    def __init__(self, ip_address: str, host_port: int = DEFAULT_PORT):
        self.ip_address = ip_address
        self.app = Flask(__name__)
        self.host_port = host_port
        self.peers = []
        self.nodes_list = {}
        self.blockchain = Blockchain()

        def add_node(node_ip, node_port):
            url = PROT + '://' + node_ip + ':' + node_port + URI_GET_STATUS

            node_status = self.get_peer_status(url)

            self.nodes_list[node_ip] = {'status': STATUS_RUNNING, 'port': node_port}
            pass

        @self.app.route(URI_GET_STATUS, methods=['GET'])
        def get_curr_status():
            return json.dumps({'UP': True}), 200, {'ContentType': 'application/json'}

        @self.app.route(URI_GET_NODES, methods=['GET'])
        def get_nodes():
            return json.dumps(self.nodes_list)

        @self.app.route(URI_ADD_NODE, methods=['GET'])
        def add_node_async():
            node_ip = request.args.get(IP_PARAM)
            node_port = request.args.get(PORT_PARAM)

            _thread.start_new_thread(add_node, (node_ip, node_port))
            return 'Successfully added.', 200

        @self.app.route(URI_GET_BLOCK, methods=['GET'])
        def get_block():
            status_code = 200
            json_string = ''
            index = request.args.get(BLOCK_INDEX_PARAM)
            try:
                block = self.blockchain.get_block(int(index))
                json_string = json.dumps(block.to_dict())
            except:
                print("Invalid block index")
                status_code = 500
            return json_string, status_code, {'ContentType': 'application/json'}
               

    def get_peer_status(self, url):
        response = requests.get(url=url)
        return STATUS_RUNNING if response.status_code == 200 else STATUS_NOT_RESPONDING

    def transmit_data(self, url, data):
        with self.app.app_context():
            requests.post(url=url, data=data)

    def transmit_json(self, url, json):
        with self.app.app_context():
            requests.post(url=url, json=json)

    def start(self):
        self.app.run(host=self.ip_address, port=self.host_port)

# def async_req(self, peer, route, payload):
#     address = PROT + peer.ip + ":" + peer.port + route
#
#     try:
#
#         _thread.start_new_thread(self.transmit_json, (address, payload))
#
#     except:
#
#         return " <h1> Data transmission failed </h1>", 400
#
#     return " <h1> Data was  sent successfully </h1>", 200
