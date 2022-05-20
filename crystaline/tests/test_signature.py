from crystaline.transaction.signature import *
from crystaline.transaction.transaction import Transaction as tr
from crystaline.public_address.public_address_generator import PublicAddressGenerator as pa
import pytest


@pytest.fixture()
def transaction():
    inputs = [
        ("test_input_address", 0)
    ]
    outputs = [
        ("test_public_address", 25)
    ]
    transaction = tr(inputs, outputs, "")

    pv_key = 123456
    transaction.sign(pv_key)

    pub_add = pa(pv_key)
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

    temp = tr([], [], "")
    temp.load(file_address)

    assert trans.get_details() == temp.get_details()
    assert trans.signature == temp.signature
    assert trans.to_json() == temp.to_json()


def test_json_format(transaction):
    trans, pub_key = transaction
    js = trans.to_json()
    print(js)
