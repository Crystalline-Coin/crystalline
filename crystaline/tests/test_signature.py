from ..transaction.Signature import *
from ..transaction import Transaction as tr
from ..public_address import public_address_generator as pa
import pytest


@pytest.fixture()
def transaction():
    # print("   0  -> exit")
    # print("   1  -> create transaction")
    # print("   2  -> sign transaction")
    # print("   3  -> get public key")
    # print("   4  -> validate signature with public key")
    # print("   5  -> print transaction details in string format(except signature)")
    # print("   6  -> print transaction inputs")
    # print("   7  -> print transaction outputs")
    # print("   8  -> print transaction signature")
    # print("   9  -> print transaction data in json format")
    # print("   10 -> save transaction to file")
    # print("   11 -> load transaction from file")
    inputs = [
        ("test_input_address", 0)
    ]
    outputs = [
        ("test_public_address", 25)
    ]
    transaction = tr.Transaction(inputs, outputs, "")

    pv_key = 123456
    transaction.sign(pv_key)

    pub_add = pa.PublicAddressGenerator(pv_key)
    pub_key = pub_add.public_key

    return transaction, pub_key


def test_verify_signature(transaction):
    trans, pub_key = transaction
    assert verify_signature(trans, pub_key)


def test_transaction_details(transaction):
    trans, pub_key = transaction
    assert trans.get_details() == "test_input_address0test_public_address25"


def test_inputs(transaction):
    trans, pub_key = transaction
    assert trans.input_address == [("test_input_address", 0)]


def test_outputs(transaction):
    trans, pub_key = transaction
    assert trans.output_address == [("test_public_address", 25)]


def test_write_and_read_from_file(transaction):
    trans, pub_key = transaction
    file_address = "test_file.txt"
    trans.save(file_address)

    temp = tr.Transaction([], [], "")
    temp.load(file_address)

    assert trans.get_details() == temp.get_details()
    assert trans.signature == temp.signature
    assert trans.to_json() == temp.to_json()


def test_json_format(transaction):
    trans, pub_key = transaction
    js = trans.to_json()
    print(js)
