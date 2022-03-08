import json
from ..block import helper as hp
from ..transaction import Signature as sg
from ..public_address import public_address_generator as pa

class Transaction: 
    def __init__(self, _input_address = None, _output_address = None, _signature = ""):
        self.input_address = _input_address
        self.output_address = _output_address
        self.signature = _signature

    def sign(self, private_key):
        if self.signature == "" :
            self.signature = sg.sign(self, private_key)

    def to_json(self):
        transactions_json = {
            "input_address" : dict(self.input_address),
            "output_address": dict(self.output_address),
            "signature" : str(self.signature) 
        }
        return json.dumps(transactions_json)

    @classmethod
    def from_json(cls, transactions_json):
        loads_transactions_json = json.loads(transactions_json)
        input_address = [(k, v) for k, v in loads_transactions_json["input_address"].items()]
        output_address = [(k, v) for k, v in loads_transactions_json["output_address"].items()]
        signature = loads_transactions_json["signature"][2:-1].encode().decode('unicode_escape').encode("raw_unicode_escape")
        return cls(input_address, output_address, signature)

    def save(self, path):
        file = open(path, "w")
        json_string = self.to_json()
        file.write(json_string)
        file.close()

    def load(self, path):
        file = open(path, "r")
        json_string = file.read()
        self.from_json(json_string)
        file.close()

    def get_details(self):
        input_address_str = ''.join([str(x) for t in self.input_address for x in t])
        output_address_str = ''.join([str(x) for t in self.output_address for x in t])
        return input_address_str + output_address_str

    def get_hash(self):
        return hp.gen_hash(self.get_details())

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(dict):
        return Transaction(dict['_input_address'], dict['_output_address'], dict['_signature'])

    def is_valid(self, public_key, blockchain):
        if sg.verify_signature(self, public_key):
            (flag, utxos_values) = self.validate_input_UTXOs(blockchain, public_key)
            if flag == True:
                if self.get_sum_of_outputs_values() <= sum(utxos_values):
                    return True
        return False

    def get_output(self, index):
        if len(self.output_address) > index:
            return self.output_address[index]
        else :
            return None

    def has_input(self, utxo):
        for i in self.input_address:
            if i == utxo:
                return True
        return False

    def validate_input_UTXOs(self, blockchain, public_key):
        utxos_values = []
        for input_add in self.input_address:
            trans_hash = input_add[0]
            output_index = input_add[1]
            temp = blockchain.get_utxo(trans_hash, output_index)
            if temp == None:
                return False, []
            else :
                (utxo, index) = temp
                utxos_values.append(utxo[1])
                if not self.utxo_belongs_to_pubkey(utxo, public_key):
                    return False, []
                elif blockchain.utxo_is_spent(index, input_add):
                    return False, []
        return True, utxos_values

    def get_sum_of_outputs_values(self):
        sum_of_values = 0
        for output in self.output_address:
            sum_of_values += output[1]
        return sum_of_values

    @staticmethod
    def utxo_belongs_to_pubkey(utxo, public_key):
        public_address = utxo[0]
        public_address_from_public_key = pa.PublicAddressGenerator.generate_public_address_from_public_key(public_key)
        if public_address == public_address_from_public_key:
            return True
        return False