import hashlib
a = bytearray(b'\0')
a.extend(hashlib.sha3_224("salam".encode()).digest()[:6])
print(int(a, 16))