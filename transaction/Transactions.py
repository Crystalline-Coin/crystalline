import json

class Transaction: 
    def __init__(self, _input_address, _output_address, _value, _signature):
        self.input_address = _input_address
        self.output_address = _output_address
        self.value = _value
        self.signature = _signature

    def save_json(self):
        transactions_json = {
            "input_address" : self.input_address,
            "output_address": self.output_address,
            "value": self.value,
            "signature" : self.signature
        }
        return transactions_json

    def to_json(self):
        return json.dumps(self.save_json())

    def load_json(self, loads_transactions_json):
        self.input_address = loads_transactions_json["input_address"]
        self.output_address = loads_transactions_json["output_address"]
        self.value = loads_transactions_json["value"]
        self.signature = loads_transactions_json["signature"]
    
    def from_json(self, transactions_json):
        self.load_json(json.loads(transactions_json))

    def is_valid(self):
        pass
