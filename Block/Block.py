import time
from crystaline.Block.helper import gen_hash_encoded
import time


class Block:
    def __init__(self, version: str, prev_hash: str, difficulty_target: int, nonce: int,
                 timestamp: time = int(time.time())):
        self.version = version
        self.prev_hash = prev_hash
        self.difficulty_target = difficulty_target
        self.nonce = nonce
        self.timestamp = timestamp

    def to_dict(self):
        return {
            'version': self.version,
            'prev_hash': self.prev_hash,
            'difficulty_target': self.difficulty_target,
            'nonce': self.nonce
        }
    
    def generate_block_hash(self):
        arr = bytearray(self.version)
        arr.extend(self.prev_hash)
        arr.extend([self.difficulty_target])
        arr.extend([self.nonce])
        arr.extend([self.timestamp])
        return gen_hash_encoded(arr)
    
    def is_valid(self):
        if(not self.version or not self.prev_hash or not self.difficulty_target or not self.nonce or not self.timestamp):
            return False
        else:
            return True
        
