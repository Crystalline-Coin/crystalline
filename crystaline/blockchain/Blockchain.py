import re
import time

from crystaline.block.Block import Block
from crystaline.fee_calculator.fee_calculator import F_x_calculator, G_x_calculator
from crystaline.block.helper import gen_hash

GENESIS_BLOCK_DIFFICULTY = 0
GENESIS_FIRST_BLOCK_DIFFICULTY = 0
GENESIS_FIRST_BLOCK_HASH = 0


class Blockchain:
    def __init__(self):
        self.chain = []
        self.all_block_hashes = []
        self.length = 0
        self.add_new_block(difficulty_target=0, transactions=[])
        self.last_force_update_status = False

    def add_new_block(self, difficulty_target, transactions):
        if len(self.chain):
            new_block = Block(
                len(self.chain),
                self.last_block.generate_block_hash(),
                difficulty_target,
                GENESIS_BLOCK_DIFFICULTY,
                time.time(),
                transactions,
            )
        else:
            new_block = Block(
                len(self.chain),
                GENESIS_FIRST_BLOCK_HASH,
                difficulty_target,
                GENESIS_FIRST_BLOCK_DIFFICULTY,
                time.time(),
                transactions,
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
            times_diffrence = now_time - self.chain[i].timestamp
            if times_diffrence > time_period:
                break
            else:
                for j in range(0, len(self.chain[i].files)):
                    if self.chain[i].files[j] == uploader_address:
                        G_x *= G_x_calculator(times_diffrence, uploaded_file_size)
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
                    if utxo == None:
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

    def get_hashed_chain(self):
        hash_list = []
        for block in self.chain:
            hash_list.append(block.generate_block_hash())
        return hash_list

    def get_hash(self):
        hash_list = self.get_hashed_chain()
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

    def get_chain(self, starting_index, ending_index):
        return self.chain[starting_index: ending_index]
