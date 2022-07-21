import re
import time
import json

from crystaline.block.block import Block
from crystaline.fee_calculator.fee_calculator import *

from crystaline.block.helper import gen_hash
from crystaline.mining_handler.mining_handler import MIDDLE_OF_96_BYTE_HASHES

GENESIS_BLOCK_DIFFICULTY = 0
GENESIS_BLOCK_HASH = "0"


class Blockchain:
    def __init__(self):
        self.chain = []
        self.all_block_hashes = []
        self.length = 0
        self.add_genesis_block()
        self.last_force_update_status = False

    def add_genesis_block(self):
        new_block = Block(
            len(self.chain),
            GENESIS_BLOCK_HASH,
            GENESIS_BLOCK_DIFFICULTY,
            GENESIS_BLOCK_DIFFICULTY,
            int(time.time()),
            [],
            [],
        )
        self.chain.append(new_block)
        self.length += 1
        return new_block

    def add_block(self, block):
        if not block.is_valid():
            return False
        self.chain.append(block)
        self.length += 1
        if not self.validate():
            self.chain.pop(-1)
            return False
        return True

    def add_new_block(self, difficulty_target, transactions, files):
        new_block = Block(
            len(self.chain),
            self.last_block.generate_block_hash(),
            difficulty_target,
            GENESIS_BLOCK_DIFFICULTY,
            time.time(),
            transactions,
            files,
        )
        self.chain.append(new_block)
        self.length += 1
        return new_block

    def validate(self):
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i - 1]
            current_block = self.chain[i]
            if previous_block.generate_block_hash() != current_block.prev_hash:
                return False
            if previous_block.timestamp > current_block.timestamp:
                return False
        return True

    def calculate_fee(self, time_period, uploaded_file_size, uploader_address):
        F_x = F_x_calculator(uploaded_file_size)
        time_period = time_period * 24 * 60 * 60
        G_x = 1
        for i in range(len(self.chain), 0, -1):
            now_time = int(time.time())
            times_difference = now_time - self.chain[i].timestamp
            if times_difference > time_period:
                break
            else:
                for j in range(0, len(self.chain[i].files)):
                    if self.chain[i].files[j] == uploader_address:
                        G_x *= G_x_calculator(times_difference, uploaded_file_size)
        fee = F_x * G_x
        return fee

    @property
    def last_block(self):
        return self.chain[-1]

    def is_block_available(self, index: int):
        if self.length <= index:
            return False
        return True

    def get_block(self, index: int):
        assert self.is_block_available(index=index)
        return self.chain[index]

    def get_utxo(self, trans_hash, output_index):
        for i in range(0, len(self.chain)):
            curr_block = self.get_block(i)
            for trans in curr_block.transactions:
                if trans.get_hash() == trans_hash:
                    utxo = trans.get_output(output_index)
                    if utxo is None:
                        return None
                    else:
                        return utxo, i
        return None

    def utxo_is_spent(self, block_index, utxo):
        for i in range(block_index + 1, len(self.chain)):
            curr_block = self.get_block(i)
            for trans in curr_block.transactions:
                if trans.has_input(utxo):
                    return True
        return False

    def get_chain_hashes(self):
        hash_list = []
        for block in self.chain:
            hash_list.append(block.generate_block_hash())
        return hash_list

    def get_chain_hashes(self, starting_index, ending_index):
        chain = self.get_chain(starting_index, ending_index)
        hashes = {}
        index = starting_index
        for block in chain:
            hashes[index] = block.generate_block_hash()
            index += 1
        return json.dumps(hashes)

    def get_hash(self):
        hash_list = self.get_chain_hashes()
        hash_list_str = ""
        for hs in hash_list:
            hash_list_str += hs
        return gen_hash(hash_list_str)

    def get_block_hashes_list(self):
        self.last_force_update_status = False
        new_chain_hashes = []
        for i in range(len(self.all_block_hashes)):
            new_chain_hashes.append(self.chain[i].generate_block_hash())
        if new_chain_hashes != self.all_block_hashes:
            self.last_force_update_status = True
            self.all_block_hashes = new_chain_hashes[:]
        for i in range(len(self.all_block_hashes), len(self.chain)):
            self.all_block_hashes.append(self.chain[i].genrate_block_hash())
        return self.all_block_hashes

    def get_last_force_update_status(self):
        return self.last_force_update_status

    def get_last_block_hash(self):
        return self.last_block.generate_block_hash()

    def get_full_chain(self) -> str:
        json_dict = {}
        for i, block in enumerate(self.chain):
            json_dict[i + 1] = block.to_dict()
        return json.dumps(json_dict)

    def get_chain(self, starting_index, ending_index):
        return self.chain[starting_index:ending_index]

    def get_difficulty_target(self):
        # TODO: COMPLETE HERE VERY IMPORTANT!
        return MIDDLE_OF_96_BYTE_HASHES
