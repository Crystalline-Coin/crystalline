import random
import sys

sys.path.insert(1, "C:/Users/Lenovo/Desktop")

from ..transaction import Transaction as tr
from ..blockchain import Blockchain as bc
from ..public_address import public_address_generator as pa
from ..block import helper as hp

print("Test transaction validation : ")

test_accounts = []

for i in range(0, 10):
    n = random.randint(1, 10000000000000000000000000000000000000000000000000000000)
    test_accounts.append(pa.PublicAddressGenerator(n))

test_blockchain = bc.Blockchain()

transactions = []
########################################################
inputs = []
inputs.append(("blockreward1", 0))
outputs = []
outputs.append((test_accounts[0].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward1", 0))
outputs = []
outputs.append((test_accounts[1].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward1", 0))
outputs = []
outputs.append((test_accounts[2].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward1", 0))
outputs = []
outputs.append((test_accounts[3].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward1", 0))
outputs = []
outputs.append((test_accounts[4].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))

test_blockchain.add_new_block(0, transactions)

print("First block added to the blockchain.")

transactions = []
########################################################
inputs = []
inputs.append(("blockreward2", 0))
outputs = []
outputs.append((test_accounts[0].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward2", 0))
outputs = []
outputs.append((test_accounts[1].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward2", 0))
outputs = []
outputs.append((test_accounts[2].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward2", 0))
outputs = []
outputs.append((test_accounts[3].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward2", 0))
outputs = []
outputs.append((test_accounts[4].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))

test_blockchain.add_new_block(0, transactions)

print("Seccond block added to the blockchain.")

transactions = []
########################################################
inputs = []
inputs.append(("blockreward3", 0))
outputs = []
outputs.append((test_accounts[0].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward3", 0))
outputs = []
outputs.append((test_accounts[1].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward3", 0))
outputs = []
outputs.append((test_accounts[2].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward3", 0))
outputs = []
outputs.append((test_accounts[3].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward3", 0))
outputs = []
outputs.append((test_accounts[4].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))

test_blockchain.add_new_block(0, transactions)

print("Third block added to the blockchain.")

transactions = []
########################################################
inputs = []
inputs.append((test_blockchain.chain[1].transactions[0].get_hash(), 0))
outputs = []
outputs.append((test_accounts[1].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward4", 0))
outputs = []
outputs.append((test_accounts[1].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward4", 0))
outputs = []
outputs.append((test_accounts[2].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward4", 0))
outputs = []
outputs.append((test_accounts[3].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))
#########################################################
inputs = []
inputs.append(("blockreward4", 0))
outputs = []
outputs.append((test_accounts[4].public_address, 25))
transactions.append(tr.Transaction(inputs, outputs))

test_blockchain.add_new_block(0, transactions)

print("Fourth block added to the blockchain.")

########################################################double_spend
print("Double spend : ")
inputs = []
inputs.append((test_blockchain.chain[1].transactions[0].get_hash(), 0))
outputs = []
outputs.append((test_accounts[0].public_address, 25))
test_transaction = tr.Transaction(inputs, outputs)
test_transaction.sign(test_accounts[0]._private_key)
print("   Verification result : ", test_transaction.is_valid(test_accounts[0].public_key, test_blockchain))
#########################################################first_input_is_valid_but_the_seccond_was_spent
print("First input is valid but the seccond was spent : ")
inputs = []
inputs.append((test_blockchain.chain[2].transactions[0].get_hash(), 0))
inputs.append((test_blockchain.chain[1].transactions[0].get_hash(), 0))
outputs = []
outputs.append((test_accounts[1].public_address, 25))
test_transaction = tr.Transaction(inputs, outputs)
test_transaction.sign(test_accounts[0]._private_key)
print("   Verification result : ", test_transaction.is_valid(test_accounts[0].public_key, test_blockchain))
#########################################################valid
print("Valid : ")
inputs = []
inputs.append((test_blockchain.chain[2].transactions[0].get_hash(), 0))
outputs = []
outputs.append((test_accounts[2].public_address, 23))
test_transaction = tr.Transaction(inputs, outputs)
test_transaction.sign(test_accounts[0]._private_key)
print("   Verification result : ", test_transaction.is_valid(test_accounts[0].public_key, test_blockchain))
#########################################################the_public_address_does_not_belong_to_this_public_key
print("The public address does not belong to this public key : ")
inputs = []
inputs.append((test_blockchain.chain[2].transactions[2].get_hash(), 0))
outputs = []
outputs.append((test_accounts[3].public_address, 23))
test_transaction = tr.Transaction(inputs, outputs)
test_transaction.sign(test_accounts[0]._private_key)
print("   Verification result : ", test_transaction.is_valid(test_accounts[0].public_key, test_blockchain))
#########################################################this_utxo_doesn't_exist
print("This UTXO doesn't exist : ")
inputs = []
inputs.append((test_blockchain.chain[2].transactions[0].get_hash(), 10))
outputs = []
outputs.append((test_accounts[4].public_address, 25))
test_transaction = tr.Transaction(inputs, outputs)
test_transaction.sign(test_accounts[0]._private_key)
print("   Verification result : ", test_transaction.is_valid(test_accounts[0].public_key, test_blockchain))
#########################################################the_transaction_hash_doesn't_valid
print("The transaction hash doesn't valid : ")
inputs = []
inputs.append((hp.gen_hash("invalid"), 0))
outputs = []
outputs.append((test_accounts[4].public_address, 25))
test_transaction = tr.Transaction(inputs, outputs)
test_transaction.sign(test_accounts[0]._private_key)
print("   Verification result : ", test_transaction.is_valid(test_accounts[0].public_key, test_blockchain))
#########################################################the_output_value_is_more_than_input
print("The output value is more than input : ")
inputs = []
inputs.append((test_blockchain.chain[2].transactions[0].get_hash(), 0))
outputs = []
outputs.append((test_accounts[4].public_address, 26))
test_transaction = tr.Transaction(inputs, outputs)
test_transaction.sign(test_accounts[0]._private_key)
print("   Verification result : ", test_transaction.is_valid(test_accounts[0].public_key, test_blockchain))
#########################################################the_signature_is_invalid
print("The signature is invalid : ")
inputs = []
inputs.append((test_blockchain.chain[2].transactions[0].get_hash(), 0))
outputs = []
outputs.append((test_accounts[2].public_address, 23))
test_transaction = tr.Transaction(inputs, outputs)
test_transaction.sign(test_accounts[1]._private_key)
print("   Verification result : ", test_transaction.is_valid(test_accounts[0].public_key, test_blockchain))
#########################################################
print("Done!")
