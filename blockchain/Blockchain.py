import time
import hashlib
from crystaline.block.Block import Block

GENESIS_FIRST_BLOCK_DIFFICULTY = 0
GENESIS_BLOCK_DIFFICULTY = 0

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.length = 0
        self.add_new_block(difficulty_target = 0)

    def add_new_block(self, difficulty_target):
        if(len(self.chain)):
            new_block = Block(len(self.chain), self.last_block.generate_block_hash(), difficulty_target, GENESIS_BLOCK_DIFFICULTY , time.time())
        else:
            new_block = Block(len(self.chain), GENESIS_FIRST_BLOCK_DIFFICULTY , difficulty_target, GENESIS_FIRST_BLOCK_DIFFICULTY , time.time())
        self.chain.append(new_block)
        self.length += 1
        return new_block

    def validate(self):
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i-1]
            current_block = self.chain[i]
            if (previous_block.generate_block_hash() != current_block.prev_hash):
                return False
            if (previous_block.timestamp > current_block.timestamp):
                return False
        return True
    
    @property
    def last_block(self):
        return self.chain[-1]

    def is_block_available(self, index : int):
        if self.length <= index:
            return False
        return True
    
    def get_block(self, index : int):
        assert self.is_block_available(index= index)
        return self.chain[index] 