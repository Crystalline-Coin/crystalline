import time
import hashlib
from crystaline.block.Block import Block
from crystaline.fee_calculator import fee_calculator

GENESIS_BLOCK_DIFFICULTY = 0
BLOCK_DIFFICULTY = 0

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.length = 0
        self.add_new_block(difficulty_target = 0)

    def add_new_block(self, difficulty_target):
        if(len(self.chain)):
            new_block = Block(len(self.chain), self.last_block.generate_block_hash(), difficulty_target, GENESIS_BLOCK_DIFFICULTY , time.time())
        else:
            new_block = Block(len(self.chain), BLOCK_DIFFICULTY , difficulty_target, BLOCK_DIFFICULTY , time.time())
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
    
        def calculate_fee(self , time_period , uploaded_file_size , uploader_address):
            F_x = F_x_calculator(uploaded_file_size)
            time_period = time_period * 24 * 60 * 60
            G_x = 1
            for i in range(len(self.chain) , 0 ,-1):
                now_time = int(time.time())
                times_diffrence  = now_time - self.chain[i].timestamp
                if(times_diffrence > time_period):
                    break
                else:
                    for j in range(0 , len(self.chain[i].files)):                      
                        if self.chain[i].files[j] == uploader_address:
                            G_x *= G_x_calculator(times_diffrence , uploaded_file_size)
            fee = F_x * G_x
            return fee
    
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
