from ecpy.curves import Curve, Point
from hashlib import sha256, sha3_224

'''Using ECPy for elliptic curve. 
More information on: 
'''
curveName = 'Ed448'

class PublicAddressGenerator:

    def __init__(self, _privateKey):
        self.privateKey = _privateKey
        self.curve = Curve.get_curve(curveName)
        self.createPublicKey()
        self.createPublicAddress()

    @staticmethod
    def hash(input):
        return 

    def createPublicKey(self):
        generator = self.curve.generator
        self.publicKey = self.privateKey * generator

    def createPublicAddress(self):
        x, y = self.publicKey.x, self.publicKey.y
        concatenation = str(x) + str(y)
