import Signature as sg
import Transaction as tr

a = tr.Transaction("in address", "out address", "value", "")

b = sg.sign(a, "private key")

print("test")

print(b)
