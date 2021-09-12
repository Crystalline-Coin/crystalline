import time
import hashlib
from crystaline.Block.Block import Block

GENESIS_FIRST_BLOCK_DIFFICULTY = 0
GENESIS_BLOCK_DIFFICULTY = 0
class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.add_new_block(difficulty_target = 0)

    def add_new_block(self, difficulty_target):
        if(len(self.chain)):
            new_block = Block(len(self.chain), self.last_block.generate_block_hash(), difficulty_target, GENESIS_BLOCK_DIFFICULTY , time.time())
        else:
            new_block = Block(len(self.chain), GENESIS_FIRST_BLOCK_DIFFICULTY , difficulty_target, GENESIS_FIRST_BLOCK_DIFFICULTY , time.time())
        self.chain.append(new_block)
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
    
    def calculate_fee(self , uploaded_file_size):
        F_x = F_x_calculator(self , uploaded_file_size)
        time_period = 30
        time_period = time_period * 24 * 60 * 60
        G_x = 1
        for i in range(len(self.chain) , 0 ,-1):
            now_time = int(time.time())
            times_diffrence  = now_time - self.chain[i].timestamp
            if(times_diffrence > time_period):
                break
            else:
                G_x *= G_x_calculator(self , times_diffrence , uploaded_file_size)
        fee = F_x * G_x
        return fee
    
    def F_x_calculator(self , uploaded_file_size):
        alpha = 2
        uploaded_file_size = 0                                                              # uploaded_file_size : S_c
        F_x = uploaded_file_size * alpha + alpha        
        for i in range(0 , int(uploaded_file_size)):                                        # applying floors
            F_x += 1
        return F_x
    
    def H_x_calculator(slef , times_diffrence):
        n = 1
        time_period = 30                                    #time_period : t
        time_period = time_period * 24 * 60 * 60
        H_x = 0
        if(times_diffrence <= time_period):
            H_x = pow(time_period/times_diffrence , n)
        else:
            H_x = 1
        return H_x
    
    def K_x_calculator(slef , file_size):
        time_period = 30                                    #file size: s
        beta = 20
        k_x = -(time_period/(file_size+(time_period/beta))) + beta
        return k_x
    
    def G_x_calculator(self , times_diffrence , file_size):
        return K_x_calculator(self , file_size) * H_x_calculator(self , times_diffrence)
    
    @property
    def last_block(self):
        return self.chain[-1]
