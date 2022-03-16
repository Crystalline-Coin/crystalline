import _thread
from flask import Flask
from flask import request, jsonify
import requests
import json
import multiprocessing

from crystaline.blockchain.Blockchain import Blockchain
from crystaline.file.file import File
from crystaline.transaction.Transaction import Transaction

DEFAULT_PROTOCOL = "http"
DEFAULT_METHODS = [["POST"], "GET"]
DEFAULT_PORT = 5000

URL_GET_STATUS = "/get_status"

STATUS_RADDR_UP = "UP"
STATUS_RADDR_DOWN = "DOWN"

PARAM_IP = "dst_ip"
PARAM_PORT = "dst_port"
PARAM_BLOCK_INDEX = "block_index"

PARAM_NODES_LIST_PORT = "port"
PARAM_NODES_LIST_STATUS = "status"


def get_peer_status(url, method):
    if ["POST"] in DEFAULT_METHODS:
        res = requests.post(url)
    elif "GET" in DEFAULT_METHODS:
        res = requests.get(url)
    else:
        raise Exception("Provided method is not consistent.")

    return STATUS_RADDR_UP if res.status_code == 200 else STATUS_RADDR_DOWN


class Node:
    def __init__(
        self,
        ip_address: str,
        host_port: int = DEFAULT_PORT,
        blockchain: Blockchain = None,
        nodes_list=None,
    ):
        if nodes_list is None:
            nodes_list = {}

        self.ip_address = ip_address
        self.host_port = host_port

        self.app = Flask(__name__)

        self.nodes_list = nodes_list
        self.blockchain = blockchain

        self.running_process = None

        self.file_pool = []
        self.transaction_pool = []

        def add_node(node_ip, node_port):
            url = DEFAULT_PROTOCOL + "://" + node_ip + ":" + node_port + URL_GET_STATUS
            node_status = get_peer_status(url, DEFAULT_METHODS[0])
            self.nodes_list[node_ip] = {
                PARAM_NODES_LIST_STATUS: node_status,
                PARAM_NODES_LIST_PORT: node_port,
            }
            # TODO: ?
            pass

        @self.app.route(URL_GET_STATUS, methods=["GET"])
        def get_curr_status():
            return json.dumps({"UP": True}), 200, {"ContentType": "application/json"}

        @self.app.route("/get_nodes", methods=["GET"])
        def get_nodes():
            return json.dumps(self.nodes_list)

        @self.app.route("/add_node", methods=["POST"])
        def add_node_async():
            node_ip = request.args.get(PARAM_IP)
            node_port = request.args.get(PARAM_PORT)

            _thread.start_new_thread(add_node, (node_ip, node_port))
            return "Successfully added.", 200

        @self.app.route("/get_block", methods=["GET"])
        def get_block():
            status_code = 200
            json_string = ""
            index = request.args.get(PARAM_BLOCK_INDEX)
            try:
                block = self.blockchain.get_block(int(index) - 1)
                json_string = json.dumps(block.to_dict())
            except:
                print("Invalid block index")
                status_code = 404
            return json_string, status_code, {"ContentType": "application/json"}

        @self.app.route("/add_file", methods=["POST"])
        def add_file():
            self.file_pool.append(File.from_json(request.get_json()))
            return "Successfully added.", 200

        @self.app.route("/add_txo", methods=["POST"])
        def add_txo():
            self.transaction_pool.append(Transaction.from_json(request.get_json()))
            return "Successfully added.", 200

        # TODO: Get transaction/file pool

        # LONG TODO: Add block

        # TODO: Get chain

        # TODO: Get Transaction

        # LONG TODO: Node saving and loading

    def transmit_data(self, url, data):
        with self.app.app_context():
            requests.post(url=url, data=data)

    def transmit_json(self, url, json):
        with self.app.app_context():
            requests.post(url=url, json=json)

    def start(self):
        flask_server_process = multiprocessing.Process(
            target=self.app.run, args=(self.ip_address, self.host_port)
        )
        flask_server_process.start()
        self.running_process = flask_server_process

    def terminate(self):
        if self.running_process == None:
            raise RuntimeError("Attempted to stop the server while not running.")
        self.running_process.terminate()
