import _thread
from flask import Flask
from flask import request, jsonify
import requests
import json
from crystaline.blockchain.blockchain import Blockchain
from crystaline.file.file import File
from crystaline.mining_handler.miner import Miner
from crystaline.transaction.transaction import Transaction
import multiprocessing

DEFAULT_PROTOCOL = "http"
DEFAULT_PORT = 5002

URL_GET_STATUS = "/get_status"

STATUS_RADDR_UP = "UP"
STATUS_RADDR_DOWN = "DOWN"

PARAM_IP = "dst_ip"
PARAM_PORT = "dst_port"
PARAM_BLOCK_INDEX = "block_index"

PARAM_START = "starting_block"
PARAM_END = "ending_block"

PARAM_TXOID = "txo_id"

PARAM_NODES_DICT_PORT = "port"
PARAM_NODES_DICT_STATUS = "status"

URL_ADD_NODE = "/add_node"
URL_GET_NODES = "/get_nodes"
URL_GET_STATUS = "/get_status"
URL_GET_BLOCK = "/get_block"
URL_ADD_TXO = "/add_txo"
URL_ADD_FILE = "/add_file"
URL_GET_FILE_POOL = "/get_file_pool"
URL_GET_TRANSACTION_POOL = "/get_transaction_pool"
URL_GET_CHAIN = "/get_chain"
URL_GET_TRANSACTION = "/get_transaction"
URL_MINE_BLOCK = "/mine_block"


def get_peer_status(url, method):
    if "POST" in method:
        res = requests.post(url)
    elif "GET" in method:
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
        nodes_dict=None,
    ):
        if nodes_dict is None:
            nodes_dict = {}

        self.ip_address = ip_address
        self.host_port = host_port

        self.app = Flask(__name__)

        self.nodes_dict = nodes_dict
        self.blockchain = blockchain

        self.running_process = None

        self.file_pool = []
        self.transaction_pool = {}

        def add_node(node_ip, node_port):
            url = DEFAULT_PROTOCOL + "://" + node_ip + ":" + node_port + URL_GET_STATUS
            node_status = get_peer_status(url, "GET")
            self.nodes_dict[node_ip] = {
                PARAM_NODES_DICT_STATUS: node_status,
                PARAM_NODES_DICT_PORT: node_port,
            }
            # TODO: ?
            pass

        @self.app.route(URL_GET_STATUS, methods=["GET"])
        def get_curr_status():
            return json.dumps({"UP": True}), 200, {"ContentType": "application/json"}

        @self.app.route(URL_GET_NODES, methods=["GET"])
        def get_nodes():
            return json.dumps(self.nodes_dict)

        @self.app.route(URL_ADD_NODE, methods=["POST"])
        def add_node_async():
            node_ip = request.args.get(PARAM_IP)
            node_port = request.args.get(PARAM_PORT)

            _thread.start_new_thread(add_node, (node_ip, node_port))
            return "Successfully added.", 200

        @self.app.route(URL_GET_BLOCK, methods=["GET"])
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

        @self.app.route(URL_ADD_FILE, methods=["POST"])
        def add_file():
            self.file_pool.append(File.from_json(request.get_json()))
            return "Successfully added.", 200

        @self.app.route(URL_ADD_TXO, methods=["POST"])
        def add_txo():
            new_transaction = Transaction.from_json(request.get_json())
            self.transaction_pool[new_transaction.get_hash()] = new_transaction
            return "Successfully added.", 200

        @self.app.route(URL_GET_FILE_POOL, methods=["GET"])
        def get_file_pool():
            file_pool = []
            for file in self.file_pool:
                file_pool.append(file.to_json())
            return json.dumps(file_pool), 200, {"ContentType": "application/json"}

        @self.app.route(URL_GET_TRANSACTION_POOL, methods=["GET"])
        def get_transaction_pool():
            transaction_pool = []
            for txo, transaction in self.transaction_pool.items():
                transaction_pool.append(transaction.to_json())
            return (
                json.dumps(transaction_pool),
                200,
                {"ContentType": "application/json"},
            )

        # LONG TODO: Add block

        @self.app.route(URL_GET_CHAIN, methods=["GET"])
        def get_chain():
            """
            Given a starting and ending block index, return the chain between them(including both).

            start: int. Starting block index.
            end: int. Ending block index.
            """

            status_code = 200
            json_string = ""

            start_index = request.args.get(PARAM_START)
            end_index = request.args.get(PARAM_END)
            try:
                json_string = self.blockchain.get_chain_hashes(
                    int(start_index) - 1, int(end_index) - 1
                )
            except:
                status_code = 404
            return json_string, status_code, {"ContentType": "application/json"}

        @self.app.route(URL_GET_TRANSACTION, methods=["GET"])
        def get_transaction():
            status_code = 200
            json_string = ""

            txo = request.args.get(PARAM_TXOID)
            try:
                transaction = self.transaction_pool[txo]
                json_string = transaction.to_json()
            except:
                status_code = 404
            return
        
        @self.app.route(URL_MINE_BLOCK, methods=["POST"])
        def mine_block():
            miner = Miner(self.blockchain, self.file_pool, self.transaction_pool)
            block = miner.mine_block()
            if (not block):
                return "mining failed, no blocks found!", 500
            return "done", 200

        # LONG TODO: Node saving and loading

    def transmit_data(self, url, data):
        with self.app.app_context():
            requests.post(url=url, data=data)

    def transmit_json(self, url, json):
        with self.app.app_context():
            requests.post(url=url, json=json)

    def start(self):
        # flask_server_process = multiprocessing.Process(
        #     target=self.app.run, args=(self.ip_address, self.host_port)
        # )
        self.app.run(host=self.ip_address, port=self.host_port)
        # flask_server_process.start()
        # self.running_process = flask_server_process

    def terminate(self):
        if self.running_process == None:
            raise RuntimeError("Attempted to stop the server while not running.")
        self.running_process.terminate()
