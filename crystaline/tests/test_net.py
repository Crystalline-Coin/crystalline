import time
from crystaline.transaction.transaction import Transaction
from crystaline.block.block import Block

import pytest

from crystaline.net.node import *

from crystaline.blockchain.blockchain import Blockchain

import json
import requests

NODE_IP_ADDR = "127.0.0.1"
NODE_PORT = 5000


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
        timeout -= 1
    raise RuntimeError("Url-wait timed out.")

def test_net_add_node(running_node):
    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method="GET",
        timeout=2,
    )

    req_add_node_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_ADD_NODE
    )
    res = requests.post(
            req_add_node_url, params={PARAM_IP: NODE_IP_ADDR, PARAM_PORT: NODE_PORT}
        )

    assert res.status_code == 200
    res.close()

    time.sleep(0.5)
    res = requests.get(
                DEFAULT_PROTOCOL
                + "://"
                + NODE_IP_ADDR
                + ":"
                + str(NODE_PORT)
                + URL_GET_NODES,
                params={PARAM_IP: NODE_IP_ADDR, PARAM_PORT: NODE_PORT},
            )

    assert res.status_code == 200

    res_dict = res.json()
    assert NODE_IP_ADDR in res_dict
    assert res_dict[NODE_IP_ADDR][PARAM_NODES_DICT_PORT] == str(NODE_PORT)
    assert res_dict[NODE_IP_ADDR][PARAM_NODES_DICT_STATUS] == STATUS_RADDR_UP
    res.close()


def test_net_get_block_state_404(running_node):
    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method="GET",
        timeout=2,
    )
    req_get_block_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_GET_BLOCK
    )

    res = requests.get(req_get_block_url, params={PARAM_BLOCK_INDEX: 1})

    assert res.status_code == 404

    res.close()


def test_net_get_chain_200(running_node_with_blockchain):
    running_node_with_blockchain.blockchain.chain.append(Block("version", "prev_hash", 1000, 999))
    running_node_with_blockchain.blockchain.chain.append(Block("version", "prev_hash", 1000, 999))


    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method="GET",
        timeout=2,
    )

    req_get_chain_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_GET_CHAIN
    )


    res = requests.get(req_get_chain_url, params={PARAM_START: 1, PARAM_END : 2})

    assert res.status_code == 200

    res_dict = res.json()
    chain = running_node_with_blockchain.blockchain.get_hashed_chain(0, 1)
    assert json.loads(chain) == res_dict
    res.close()

def test_net_get_block_state_200(running_node_with_blockchain):
    wait_for_url(
        url=DEFAULT_PROTOCOL
        + "://"
        + NODE_IP_ADDR
        + ":"
        + str(NODE_PORT)
        + URL_GET_STATUS,
        method="GET",
        timeout=2,
    )
    req_get_block_url = (
        DEFAULT_PROTOCOL + "://" + NODE_IP_ADDR + ":" + str(NODE_PORT) + URL_GET_BLOCK
    )

    res = requests.get(req_get_block_url, params={PARAM_BLOCK_INDEX: 1})

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
        method="GET",
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

    res = requests.post(
            req_add_file_url,
            json=json.dumps(sample_file),
            headers={"ContentType": "application/json"},
        )

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
        method="GET",
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

    res = requests.post(
            req_add_txo_url,
            json=json.dumps(sample_txo),
            headers={"ContentType": "application/json"},
        )

    assert res.status_code == 200
    res.close()
