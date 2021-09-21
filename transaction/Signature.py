import Transaction as tr
import hashlib as hl
from ecpy.ecdsa import ECDSA
from ecpy.curves import Curve, Point
from ecpy.keys import ECPublicKey, ECPrivateKey

CURVE_NAME = 'Ed448'

def sign(transaction, privatekey):
    
    transaction_details = transaction.get_details()
    trans_hash = hl.sha256(
                        transaction_details.encode()
                    ).digest()
    
    curve = Curve.get_curve(CURVE_NAME)
    private_key = ECPrivateKey(privatekey, curve)
    
    signer = ECDSA()
    signature = signer.sign(trans_hash, private_key)
    
    return signature

def verify_signature(transaction, publickey):
    
    transaction_details = transaction.get_details()
    trans_hash = hl.sha256(
                        transaction_details.encode()
                    ).digest()

    public_key = ECPublicKey(publickey)

    signer = ECDSA()
    signature = transaction.signature
    
    return signer.verify(trans_hash ,signature ,public_key)