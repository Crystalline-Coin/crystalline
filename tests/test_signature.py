from transaction import Signature as sg
from transaction import Transaction as tr
from transaction import public_address_generator as pa
from public_address.public_address_generator import PublicAddressGenerator

a = tr.Transaction("in address", "out address", "value", "")

b = sg.sign(a, 45376987097)

print(b)

a.signature = b

pub_add = pa.PublicAddressGenerator(45376987097)

pub_key = pub_add.public_key

print(pub_key)

pub_key_invalid = pa.PublicAddressGenerator(45376987098).public_key

v = sg.verify_signature(a, pub_key)

print(v)

invalid = sg.verify_signature(a, pub_key_invalid)

print(invalid)
