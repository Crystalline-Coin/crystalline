import time
import hashlib
from crystaline.Block.Block import Block

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.add_new_block(difficulty_target = 0)
        
    def add_new_block(self, difficulty_target):
        if(len(self.chain)):
            new_block = Block(len(self.chain), self.last_block.generate_block_hash(), difficulty_target, 0, time.time())
        else:
            new_block = Block(len(self.chain), 0, difficulty_target, 0, time.time())
        self.chain.append(new_block)
        return new_block

    def validate(self):
        for i in range(1, len(self.chain)):
            previous_block = self.chain[i-1]
            current_block = self.chain[i]
            if (previous_block.generate_block_hash() != current_block.prev_hash):
                return False
            if ((current_block.version != previous_block.version + 1) or (previous_block.timestamp > current_block.timestamp)):
                return False
        return True
    
    @property
    #Shouldn't the name be get_last_block?
    def last_block(self):
        return self.chain[-1]
    def get_block_hash_list(self):
       return [element.generate_block_hash() for element in self.chain]
