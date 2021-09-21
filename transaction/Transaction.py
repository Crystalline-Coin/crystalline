import json

class Transaction: 
    def __init__(self, _input_address, _output_address, _value, _signature):
        self.input_address = _input_address
        self.output_address = _output_address
        self.value = _value
        self.signature = _signature

    def to_json(self):
        transactions_json = {
            "input_address" : self.input_address,
            "output_address": self.output_address,
            "value": self.value,
            "signature" : self.signature
        }
        return json.dumps(transactions_json)

    def from_json(self, transactions_json):
        loads_transactions_json = json.loads(transactions_json)
        self.input_address = loads_transactions_json["input_address"]
        self.output_address = loads_transactions_json["output_address"]
        self.value = loads_transactions_json["value"]
        self.signature = loads_transactions_json["signature"]

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
        return self.input_address + self.output_address + self.value

    def is_valid(self):
        pass
