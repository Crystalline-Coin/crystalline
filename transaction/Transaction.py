import json
import crystaline.block.helper as hp
import crystaline.transaction.Signature as sg

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

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(dict):
        return Transaction(dict['_input_address'], dict['_output_address'], dict['_signature'])

    def is_valid(self, public_key, blockchain):
        if sg.verify_signature(self, public_key):
            (flag, utxos_values) = self.validate_input_UTXOs(blockchain)
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

    def validate_input_UTXOs(self, blockchain):
        utxos_values = []
        for input_add in self.input_address:
            trans_hash = input_add[0]
            output_index = input_add[1]
            temp = blockchain.get_utxo(trans_hash, output_index)
            if temp == None:
                return tuple(False, [])
            else :
                (utxo, index) = temp
                utxos_values.append(utxo[1])
                if blockchain.utxo_is_spent(index, input_add):
                    return tuple(False, [])
        return tuple(True, utxos_values)

    def get_sum_of_outputs_values(self):
        sum_of_values = 0
        for output in self.output_address:
            sum_of_values += output[1]
        return sum_of_values