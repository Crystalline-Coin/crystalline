import time
from helper import gen_hash_encoded
from pathlib import Path
from ..file.file import File

class Block:
    def __init__(self, version: str, prev_hash: str, difficulty_target: int, nonce: int,
                 timestamp: time = int(time.time())):
        self.version = version
        self.prev_hash = prev_hash
        self.difficulty_target = difficulty_target
        self.nonce = nonce
        self.timestamp = timestamp
        self.files = []

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
