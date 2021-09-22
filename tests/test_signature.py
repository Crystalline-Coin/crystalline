from crystaline.transaction import Signature as sg
from crystaline.transaction import Transaction as tr
from crystaline.public_address import public_address_generator as pa

#a = tr.Transaction([("ali", 23)], [("sdzdzg", 1), ("sddn", 3.4523), ("ksdnf", 0.0001)], "")
##js = a.to_json()
##print(js)
##a.save("json.txt")
##a2 = tr.Transaction([], [], "")
##a2.load("json.txt")
##print(a2.input_address)
##print(a2.output_address)

#b = sg.sign(a, 45376987097)

##print(b)

#a.signature = b

#pub_add = pa.PublicAddressGenerator(45376987097)

#pub_key = pub_add.public_key

##print(pub_key)

#pub_key_invalid = pa.PublicAddressGenerator(45376987098).public_key

#v = sg.verify_signature(a, pub_key)

##print(v)

##invalid = sg.verify_signature(a, pub_key_invalid)

##print(invalid)

##print(a.input_address)
##print(a.output_address)

#js = a.to_json()

#print(js)

##a.save("json.txt")

##a2 = tr.Transaction([], [], "")

##a2.load("json.txt")

##print(a2.input_address)
##print(a2.output_address)

a = tr.Transaction([("ali", 23)], [("sdzdzg", 1), ("sddn", 3.4523), ("ksdnf", 0.0001)], "")

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

print(a.get_details())
print(a.input_address)
print(a.output_address)

js = a.to_json()

print(js)

a.save("json.txt")

a2 = tr.Transaction([], [], "")

a2.load("json.txt")

print(a2.input_address)
print(a2.output_address)
print(a2.signature)