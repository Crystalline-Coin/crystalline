import json
import crystaline.block.helper as hp

class Transaction: 
    def __init__(self, _input_address, _output_address, _signature):
        self.input_address = _input_address
        self.output_address = _output_address
        self.signature = _signature

    def to_json(self):
        transactions_json = {
            "input_address" : dict(self.input_address),
            "output_address": dict(self.output_address),
            "signature" : str(self.signature) 
        }
        return json.dumps(transactions_json)

    def from_json(self, transactions_json):
        loads_transactions_json = json.loads(transactions_json)
        self.input_address = [(k, v) for k, v in loads_transactions_json["input_address"].items()]
        self.output_address = [(k, v) for k, v in loads_transactions_json["output_address"].items()]
        self.signature = loads_transactions_json["signature"][2:-1].encode().decode('unicode_escape').encode("raw_unicode_escape")

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

    def is_valid(self, public_key):
        pass
        