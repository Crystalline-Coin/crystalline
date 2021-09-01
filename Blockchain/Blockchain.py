import time
import hashlib
from crystaline.Block.Block import Block


GENESIS_BLOCK_DIFFICULTY = 0
NONCE = 0 
ZERO = 0

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.add_new_block(difficulty_target = 0)

    def add_new_block(self, difficulty_target):
        if(len(self.chain)):
            new_block = Block(len(self.chain), self.last_block.generate_block_hash(), difficulty_target, NONCE , time.time())
        else:
            new_block = Block(len(self.chain), ZERO , difficulty_target, GENESIS_BLOCK_DIFFICULTY , time.time())
        self.chain.append(new_block)
        return new_block

    def validate(self):
        if (self.chain[0].is_valid() == False):                                            #use this line here because first block doesn't be checked in next loop
            return False
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i-1]
            current_block = self.chain[i]
            if (current_block.is_valid() == False):
                return False
            if (previous_block.generate_block_hash() != current_block.prev_hash):
                return False
            if (previous_block.timestamp > current_block.timestamp):
                return False
        return True
    
    @property
    def last_block(self):
        return self.chain[-1]
