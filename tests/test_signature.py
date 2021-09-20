import os
import sys
current_path = os.path.abspath(os.path.dirname(__file__)) 
sys.path.append(current_path) 
project_dir = str(current_path)
sys.path.append('../public_address/')
print(sys.path)
from public_address.public_address_generator import PublicAddressGenerator
import sys
sys.path.append('../transaction/')
from transaction import Signature as sg
from transaction import Transaction as tr
from transaction import public_address_generator as pa

#import Signature as sg
#import Transaction as tr
#import public_address_generator as pa

print("test")

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
