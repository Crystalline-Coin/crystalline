import pytest
import random
from crystaline.public_address import public_address_generator as pa
from crystaline.blockchain.blockchain import Blockchain as bc
from crystaline.transaction.transaction import Transaction as tr


@pytest.fixture
def accounts():
    print("Test transaction validation : ")
    test_accounts = []

    for i in range(0, 10):
        n = random.randint(1, 10000000000000000000000000000000000000000000000000000000)
        test_accounts.append(pa.PublicAddressGenerator(n))
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

    inputs = [(test_blockchain.chain[1].transactions[0].get_hash(), 0)]
    outputs = [(test_accounts[0].public_address, 25)]
    first_transaction = tr(inputs, outputs)
    first_transaction.sign(test_accounts[0].private_key)
    test_blockchain.add_new_block(0, [first_transaction], [])

    return test_blockchain, test_accounts


def test_add_block(blockchain):
    test_blockchain, test_accounts = blockchain
    inputs = [(test_blockchain.chain[1].transactions[0].get_hash(), 0)]
    outputs = [(test_accounts[0].public_address, 25)]
    first_transaction = tr(inputs, outputs)
    first_transaction.sign(test_accounts[0].private_key)
    test_blockchain.add_new_block(0, [first_transaction], [])


def test_validate(blockchain):
    test_blockchain, test_accounts = blockchain
    assert test_blockchain.validate()
