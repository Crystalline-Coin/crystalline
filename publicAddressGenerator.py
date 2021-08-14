from hashlib import sha256, sha3_224
from fastecdsa.fastecdsa.curve import Curve

class PublicAddressGenerator:
    def __init__(self, privateKey):
        self.privateKey = privateKey
        self.curve = Curve(
            'P521',
            int('68647976601306097149819007990813932172694353001433054093944634591855431833976560521225596'
                '40661454554977296311391480858037121987999716643812574028291115057151'),
            -3,
            int('10938490380737342745111123907668055699362075989516837489945863944959531161507350160137087'
                '37573759623248592132296706313309438452531591012912142327488478985984'),
            int('68647976601306097149819007990813932172694353001433054093944634591855431833976553942450577'
                '46333217197532963996371363321113864768612440380340372808892707005449'),
            int('26617408020502170632287687167233609607298591687569731477066713684188029449964278084915450'
                '80627771902352094241225065558662157113545570916814161637315895999846'),
            int('37571800257700204635455072244911836035944551347697624866945677796155444774405563166912344'
                '05012945539562144444537289428522585666729196580810124344277578376784'),
            b'\x2B\x81\x04\x00\x23'
        )

    def createPublicKey(self):
        g = self.curve.G
        self.publicKey = g * self.privateKey

    def createPublicAddress(self):
        x, y = self.publicKey.x, self.publicKey.y
        concatenation = str(x) + str(y)
        hashed = sha3_224(sha256(concatenation.encode()))
        prefix = self.prefix
        checkSum = sha3_224(sha256(prefix + hashed))
        rawPublicAddress = prefix + hashed + checkSum
        self.publicAddress = self.encode(rawPublicAddress)

    def encode(self, rawAddress):
        pass

    def getPublicKey(self):
        return self.publicKey

    def getPublicAddress(self):
        return self.publicAddress

if __name__ == "__main__":
    generator = PublicAddressGenerator(2)
    generator.createPublicKey()
    generator.createPublicAddress()
