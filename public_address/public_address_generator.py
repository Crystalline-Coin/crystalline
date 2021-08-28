from ecpy.curves import Curve, Point
from hashlib import sha256, sha3_224

'''Using ECPy for elliptic curve. 
More information on: 
'''


class PublicAddressGenerator:

    def __init__(self, _private_key):
        curve_name = 'Ed448'
        self.private_key = _private_key
        self.curve = Curve.get_curve(curve_name)
        self.create_public_key()
        self.create_public_address()

    @staticmethod
    def hash(input):
        return sha3_224(sha256(input).digest()).digest()

    def create_public_key(self):
        generator = self.curve.generator
        self.publicKey = self.privateKey * generator

    def create_public_address(self):
        encoding = 'utf-8'
        x, y = self.publicKey.x, self.publicKey.y
        concatenation = str(x) + str(y)
        hashValue = self.hash(concatenation.encode(encoding))