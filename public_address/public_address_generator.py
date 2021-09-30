from ecpy.curves import Curve, Point
from hashlib import sha256, sha3_224


'''Using ECPy for elliptic curve. 
More information on: https://ec-python.readthedocs.io/en/latest/
'''


'''Generating 1000 addresses in about 0.54s(tested 3 times for better results).
So generating an address takes about 0.00054s on average.
'''
ENCODING = 'utf-8'
VERSION_BYTE = '00'
CURVE_NAME = 'Ed448'


class PublicAddressGenerator:

    def __init__(self, private_key):
        self._private_key = private_key
        self._curve = Curve.get_curve(CURVE_NAME)
        self.create_public_key()
        self.create_public_address()

    @staticmethod
    def main_hash(input):
        raw_value = sha3_224(sha256(input).digest()).digest()
        return raw_value.hex()
        
    @staticmethod
    def get_checksum(input):
        raw_value = sha3_224(sha3_224(input).digest()).digest()
        return raw_value[:6].hex()

    @staticmethod
    def base_represent(input):
        ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        BASE = 58
        represent = ''
        leading_ones = (len(input) - len(input.lstrip('0'))) // 2 
        address = int(input, 16)
        while address > 0:
            represent = ALPHABET[address % BASE] + represent
            address //= BASE
        return ''.join('1' for i in range(leading_ones)) \
                + represent
    
    @staticmethod
    def generate_public_address_from_public_key(public_key):
        x, y = public_key.x, public_key.y
        concatenation = str(x) + str(y)
        hash_value = PublicAddressGenerator.main_hash(concatenation.encode(ENCODING))
        address = VERSION_BYTE + hash_value
        address += PublicAddressGenerator.get_checksum(bytes.fromhex(address)) 
        return PublicAddressGenerator.base_represent(address)

    def create_public_key(self):
        generator = self._curve.generator
        self._public_key = self._private_key * generator

    def create_public_address(self):
        x, y = self._public_key.x, self._public_key.y
        concatenation = str(x) + str(y)
        hash_value = self.main_hash(concatenation.encode(ENCODING))
        address = VERSION_BYTE + hash_value
        address += self.get_checksum(bytes.fromhex(address)) 
        self._public_address = self.base_represent(address)

    @property
    def public_key(self):
        return self._public_key
    

    @property
    def public_address(self):
        return self._public_address
