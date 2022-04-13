import time
from crystaline.transaction.Transaction import Transaction

import pytest

from crystaline.net.node import Node
from crystaline.net.node import DEFAULT_PROTOCOL, DEFAULT_METHODS
from crystaline.net.node import (
    URL_ADD_NODE,
    URL_GET_NODES,
    URL_GET_STATUS,
    URL_GET_BLOCK,
    URL_ADD_TXO,
    URL_ADD_FILE,
    URL_GET_FILE_POOL,
    URL_GET_TRANSACTION_POOL,
    URL_GET_CHAIN,
    URL_GET_TRANSACTION,
)
from crystaline.net.node import (
    PARAM_IP,
    PARAM_PORT,
    PARAM_BLOCK_INDEX,
    PARAM_NODES_LIST_STATUS,
    PARAM_NODES_LIST_PORT,
    PARAM_START,
    PARAM_END,
    PARAM_TXOID,
)
from crystaline.net.node import STATUS_RADDR_UP
from crystaline.net.node import get_peer_status

from crystaline.blockchain.Blockchain import Blockchain

import json
import requests

NODE_IP_ADDR = "127.0.0.1"
NODE_PORT = 4400


@pytest.fixture
def node():
    return Node(NODE_IP_ADDR, NODE_PORT)


@pytest.fixture
def node_with_blockchain():
    blockchain = Blockchain()
    return Node(NODE_IP_ADDR, NODE_PORT, blockchain=blockchain)


@pytest.fixture
def running_node(node):
    node.start()
    yield node
    node.terminate()


@pytest.fixture
def running_node_with_blockchain(node_with_blockchain):
    node_with_blockchain.start()
    yield node_with_blockchain
    node_with_blockchain.terminate()


def wait_for_url(url: str, method: str, timeout: float):
    status = get_peer_status(url, method)
    while timeout > 0:
        if status == STATUS_RADDR_UP:
            return
        time.sleep(timeout / 4)
    raise RuntimeError("Url-wait timed out.")


def test_net_add_node(running_node):
    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method=DEFAULT_METHODS[0],
        timeout=2,
    )

    req_add_node_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_ADD_NODE
    )
    if "POST" in DEFAULT_METHODS:
        res = requests.post(
            req_add_node_url, params={PARAM_IP: NODE_IP_ADDR, PARAM_PORT: NODE_PORT}
        )
    elif "GET" in DEFAULT_METHODS:
        res = requests.get(
            req_add_node_url, params={PARAM_IP: NODE_IP_ADDR, PARAM_PORT: NODE_PORT}
        )
    else:
        raise Exception("No consistent RESTful methods used.")

    assert res.status_code == 200
    res.close()

    time.sleep(0.5)
    if "POST" in DEFAULT_METHODS:
        res = requests.post(
            DEFAULT_PROTOCOL
            + "://"
            + NODE_IP_ADDR
            + ":"
            + str(NODE_PORT)
            + URL_GET_NODES,
            params={PARAM_IP: NODE_IP_ADDR, PARAM_PORT: NODE_PORT},
        )
    elif "GET" in DEFAULT_METHODS:
        res = requests.get(
            DEFAULT_PROTOCOL
            + "://"
            + NODE_IP_ADDR
            + ":"
            + str(NODE_PORT)
            + URL_GET_NODES,
            params={PARAM_IP: NODE_IP_ADDR, PARAM_PORT: NODE_PORT},
        )
    else:
        raise Exception("No consistent RESTful methods used.")

    assert res.status_code == 200

    res_dict = res.json()
    assert NODE_IP_ADDR in res_dict
    assert res_dict[NODE_IP_ADDR][PARAM_NODES_LIST_PORT] == str(NODE_PORT)
    assert res_dict[NODE_IP_ADDR][PARAM_NODES_LIST_STATUS] == STATUS_RADDR_UP
    res.close()


def test_net_get_block_state_404(running_node):
    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method=DEFAULT_METHODS[0],
        timeout=2,
    )
    req_get_block_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_GET_BLOCK
    )

    if "POST" in DEFAULT_METHODS:
        res = requests.post(req_get_block_url, params={PARAM_BLOCK_INDEX: 1})
    elif "GET" in DEFAULT_METHODS:
        res = requests.get(req_get_block_url, params={PARAM_BLOCK_INDEX: 1})
    else:
        raise Exception("No consistent RESTful methods used.")

    assert res.status_code == 404

    res.close()


def test_net_get_chain_200(running_node_with_blockchain):
    running_node_with_blockchain.blockchain.chain.append()


    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method=DEFAULT_METHODS[0],
        timeout=2,
    )

    req_get_chain_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_GET_CHAIN + "?" + PARAM_START + "=1" + "&" + PARAM_END + "=2"
    )


    if "POST" in DEFAULT_METHODS:
        res = requests.post(req_get_chain_url, params={PARAM_BLOCK_INDEX: 1})
    elif "GET" in DEFAULT_METHODS:
        res = requests.get(req_get_chain_url, params={PARAM_BLOCK_INDEX: 1})
    else:
        raise Exception("No consistent RESTful methods used.")

    assert res.status_code == 200

    res_dict = res.json()
    assert res_dict["index"] == 1
    assert res_dict["previous_hash"] == "0"
    assert res_dict["timestamp"] == 0
    assert res_dict["data"] == "0"
    assert res_dict["hash"] == "0"
    res.close()

def test_net_get_block_state_200(running_node_with_blockchain):
    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method=DEFAULT_METHODS[0],
        timeout=2,
    )
    req_get_block_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_GET_BLOCK
    )

    if "POST" in DEFAULT_METHODS:
        res = requests.post(req_get_block_url, params={PARAM_BLOCK_INDEX: 1})
    elif "GET" in DEFAULT_METHODS:
        res = requests.get(req_get_block_url, params={PARAM_BLOCK_INDEX: 1})
    else:
        raise Exception("No consistent RESTful methods used.")

    assert res.status_code == 200
    res.close()


def test_net_add_file_state_200(running_node_with_blockchain):
    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method=DEFAULT_METHODS[0],
        timeout=2,
    )
    req_add_file_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_ADD_FILE
    )
    sample_file = {
        "_content": "content",
        "_name": "file_name",
        "_creator": "file_creator",
        "_creation_transaction": "transaction",
    }

    if "POST" in DEFAULT_METHODS:
        res = requests.post(
            req_add_file_url,
            json=json.dumps(sample_file),
            headers={"ContentType": "application/json"},
        )
    elif "GET" in DEFAULT_METHODS:
        res = requests.get(
            req_add_file_url,
            json=json.dumps(sample_file),
            headers={"ContentType": "application/json"},
        )
    else:
        raise Exception("No consistent RESTful methods used.")

    assert res.status_code == 200
    res.close()


def test_net_add_txo_state_200(running_node_with_blockchain):
    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method=DEFAULT_METHODS[0],
        timeout=2,
    )
    req_add_txo_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_ADD_TXO
    )
    sample_txo = {
        "input_address": {"1": "2"},
        "output_address": {"1": "2"},
        "signature": "signature",
    }

    if "POST" in DEFAULT_METHODS:
        res = requests.post(
            req_add_txo_url,
            json=json.dumps(sample_txo),
            headers={"ContentType": "application/json"},
        )
    elif "GET" in DEFAULT_METHODS:
        res = requests.get(
            req_add_file_url,
            json=json.dumps(sample_txo),
            headers={"ContentType": "application/json"},
        )
    else:
        raise Exception("No consistent RESTful methods used.")

    assert res.status_code == 200
    res.close()
