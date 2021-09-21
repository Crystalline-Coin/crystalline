
import time
from helper import gen_hash_encoded
from pathlib import Path
from ..file.file import File
import json

FILE_NAME_PREFIX = 'cry_'
FILE_EXTENSION = '.blk'
BYTE=8
BLOCK_FILE_SIZE = 3*1024*1024
BLOCK_TRANSACTION_SIZE = 1*1024*1024

class Block:
    def __init__(self, version: str, prev_hash: str, difficulty_target: int, nonce: int,
                 timestamp: time = int(time.time()), files = None):
        self.version = version
        self.prev_hash = prev_hash
        self.difficulty_target = difficulty_target
        self.nonce = nonce
        self.timestamp = timestamp
        if files is None:
            self.files = []
        else:
            self.files = list(files)

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

    def upload_file(self, file_path):
        path = Path(file_path)
        with open(file_path, mode='rb') as new_file:
            new_file = File(new_file.read(), path.name)
            self.files.append(new_file)

    def download_file(self, file_path, file_index):
        file = self.files[file_index]
        new_path = file_path + '/' + file.name
        with open(new_path, mode='wb') as new_file:
            new_file.write(file.content)
    
    def is_block_size_valid(self, block_size):
        if(block_size <= BLOCK_TRANSACTION_SIZE + BLOCK_FILE_SIZE):
            return False
        else:
            return True  

    def save(self, file_path):
        first_part_dict = self.to_dict()
        files_dict = {
            'files' : []
        }
        for file in self.files:
            files_dict['files'].append(file.to_dict())
        path = file_path + '/' + FILE_NAME_PREFIX \
                + str(self.timestamp) + FILE_EXTENSION
        json_string = json.dumps(first_part_dict.update(files_dict))
        with open(path, mode='w') as file:
            file.write(json_string)

    @staticmethod
    def load(file_path):
        STARTING_INDEX = len(FILE_NAME_PREFIX)
        ENDING_INDEX = -len(FILE_EXTENSION)
        with open(file_path, mode='r') as new_file:
            block_dict = json.loads(new_file.read())
        block_files = []
        for file in block_dict['files']:
            block_files.append(File.from_dict(file))
        name = Path(file_path).name
        timestamp = int(name[STARTING_INDEX:ENDING_INDEX])
        return Block(block_dict['version'], block_dict['prev_hash'],
                    block_dict['difficulty_target'], block_dict['nonce'],
                    timestamp, block_files)


