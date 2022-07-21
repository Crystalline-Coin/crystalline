import random
import pytest

from crystaline.transaction.transaction import Transaction as tr
from crystaline.blockchain.blockchain import Blockchain as bc
from crystaline.public_address.public_address_generator import (
    PublicAddressGenerator as pa,
)
from crystaline.block import helper as hp


@pytest.fixture
def accounts():
    print("Test transaction validation : ")
    test_accounts = []

    for i in range(0, 10):
        n = random.randint(1, 10000000000000000000000000000000000000000000000000000000)
        test_accounts.append(pa(n))
    return test_accounts


@pytest.fixture
def blockchain(accounts):
    test_accounts = accounts
    test_blockchain = bc()

    for k in range(1, 5):
        transactions = []
        reward = "block_reward_" + str(k)
        inputs = [(reward, 0)]
        for i in range(0, 5):
            outputs = [(test_accounts[i].public_address, 25)]
            transactions.append(tr(inputs, outputs))

        test_blockchain.add_new_block(0, transactions, [])

    inputs = [(test_blockchain.chain[1]._transactions[0].get_hash(), 0)]
    outputs = [(test_accounts[0].public_address, 25)]
    first_transaction = tr(inputs, outputs)
    first_transaction.sign(test_accounts[0].private_key)
    test_blockchain.add_new_block(0, [first_transaction], [])

    return test_blockchain, test_accounts


def test_double_spend(blockchain):
    test_blockchain, test_accounts = blockchain
    inputs = [(test_blockchain.chain[1]._transactions[0].get_hash(), 0)]
    outputs = [(test_accounts[2].public_address, 25)]
    double_spent_transaction = tr(inputs, outputs)
    double_spent_transaction.sign(test_accounts[0].private_key)
    assert not double_spent_transaction.is_valid(
        test_accounts[0].public_key, test_blockchain
    )


def test_first_input_is_valid_but_the_second_was_spent(blockchain):
    test_blockchain, test_accounts = blockchain
    inputs = [
        (test_blockchain.chain[2]._transactions[0].get_hash(), 0),
        (test_blockchain.chain[1]._transactions[0].get_hash(), 0),
    ]
    outputs = [(test_accounts[1].public_address, 25)]
    test_transaction = tr(inputs, outputs)
    test_transaction.sign(test_accounts[0].private_key)
    assert not test_transaction.is_valid(test_accounts[0].public_key, test_blockchain)


def test_public_address_does_not_belong_to_this_public_key(blockchain):
    test_blockchain, test_accounts = blockchain
    inputs = [(test_blockchain.chain[2]._transactions[2].get_hash(), 0)]
    outputs = [(test_accounts[3].public_address, 23)]
    test_transaction = tr(inputs, outputs)
    test_transaction.sign(test_accounts[0].private_key)
    assert not test_transaction.is_valid(test_accounts[0].public_key, test_blockchain)


def test_this_utxo_doesnt_exist(blockchain):
    test_blockchain, test_accounts = blockchain
    inputs = [(test_blockchain.chain[2]._transactions[0].get_hash(), 10)]
    outputs = [(test_accounts[4].public_address, 25)]
    test_transaction = tr(inputs, outputs)
    test_transaction.sign(test_accounts[0].private_key)
    assert not test_transaction.is_valid(test_accounts[0].public_key, test_blockchain)


def test_invalid_transaction_hash(blockchain):
    test_blockchain, test_accounts = blockchain
    inputs = [(hp.gen_hash("invalid!"), 0)]
    outputs = [(test_accounts[4].public_address, 25)]
    test_transaction = tr(inputs, outputs)
    test_transaction.sign(test_accounts[0].private_key)
    assert not test_transaction.is_valid(test_accounts[0].public_key, test_blockchain)


def test_output_value_more_than_input(blockchain):
    test_blockchain, test_accounts = blockchain
    print("The output value is more than input : ")
    inputs = [(test_blockchain.chain[2]._transactions[0].get_hash(), 0)]
    outputs = [(test_accounts[4].public_address, 26)]
    test_transaction = tr(inputs, outputs)
    test_transaction.sign(test_accounts[0].private_key)
    assert not test_transaction.is_valid(test_accounts[0].public_key, test_blockchain)


def test_invalid_signature(blockchain):
    test_blockchain, test_accounts = blockchain
    inputs = [(test_blockchain.chain[2]._transactions[0].get_hash(), 0)]
    outputs = [(test_accounts[2].public_address, 23)]
    test_transaction = tr(inputs, outputs)
    test_transaction.sign(test_accounts[1].private_key)
    assert not test_transaction.is_valid(test_accounts[0].public_key, test_blockchain)


def test_valid_transaction(blockchain):
    test_blockchain, test_accounts = blockchain
    inputs = [(test_blockchain.chain[2]._transactions[0].get_hash(), 0)]
    outputs = [(test_accounts[2].public_address, 23)]
    test_transaction = tr(inputs, outputs)
    test_transaction.sign(test_accounts[0]._private_key)
    assert test_transaction.is_valid(test_accounts[0].public_key, test_blockchain)
