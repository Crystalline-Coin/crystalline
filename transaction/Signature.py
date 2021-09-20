import Transaction as tr
import hashlib as hl

def sign(transaction, privatekey):
    transaction_details = transaction.input_address + transaction.output_address + transaction.value
    z = hl.sha256(transaction_details.encode()).hexdigest()
    return z