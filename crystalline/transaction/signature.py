from ecpy.ecdsa import ECDSA
from ecpy.curves import Curve, Point
from ecpy.keys import ECPublicKey, ECPrivateKey
from crystalline.public_address.public_address_generator import CURVE_NAME, ENCODING


def sign(transaction, privatekey):
    trans_hash = transaction.get_hash()

    curve = Curve.get_curve(CURVE_NAME)
    private_key = ECPrivateKey(privatekey, curve)

    signer = ECDSA()
    signature = signer.sign(bytearray(trans_hash, encoding=ENCODING), private_key)

    return signature


def verify_signature(transaction, publickey):
    trans_hash = transaction.get_hash()

    public_key = ECPublicKey(publickey)

    signer = ECDSA()
    signature = transaction.signature

    return signer.verify(bytearray(trans_hash, encoding=ENCODING), signature, public_key)
