import os.path

from ..block.helper import gen_hash
from ..file.file import File
from ..transaction.Transaction import Transaction
from pathlib import Path
import json
import time


class Block:
    FILE_NAME_PREFIX = 'cry_'
    FILE_EXTENSION = '.blk'
    BLOCK_FILE_SIZE = 3 * 1024 * 1024
    BLOCK_TRANSACTION_SIZE = 1 * 1024 * 1024
    STRING_FORMAT = 'utf-8'

    PARAM_VERSION, PARAM_PREV_HASH, PARAM_DIFF_TARGET, PARAM_NONCE, PARAM_FILES, PARAM_TRANSACTIONS, = \
        '_version', '_prev_hash', '_difficulty_target', '_nonce', '_files', '_transactions'

    def __init__(self, version: str, prev_hash: str, difficulty_target: int, nonce: int,
                 timestamp: time = int(time.time()), transactions=None, files=None):
        self._version = version
        self._prev_hash = prev_hash
        self._difficulty_target = difficulty_target
        self._nonce = nonce
        self._timestamp = timestamp
        if transactions is None:
            self._transactions = []
        else:
            self._transactions = list(transactions)
        if files is None:
            self._files = []
        else:
            self._files = list(files)
        if transactions is None:
            self._transactions = []
        else:
            self._transactions = list(transactions)

    @property
    def version(self):
        return self._version

    @property
    def prev_hash(self):
        return self._prev_hash

    @property
    def difficulty_target(self):
        return self._difficulty_target

    @property
    def nonce(self):
        return self._nonce

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def transactions(self):
        return self._transactions

    @property
    def files(self):
        return self._files

    def to_dict(self):
        block_dict = {self.PARAM_VERSION: self.version, self.PARAM_PREV_HASH: self._prev_hash,
                      self.PARAM_DIFF_TARGET: self._difficulty_target, self.PARAM_NONCE: self._nonce,
                      self.PARAM_FILES: self._files, self.PARAM_TRANSACTIONS: self._transactions}
        # for transaction in self._transactions:
        #     block_dict['transactions'].append(transaction.to_dict())
        # block_dict['files'] = []
        # for file in self._files:
        #     block_dict['files'].append(file.to_dict())
        return block_dict

    def generate_block_hash(self):
        data_string = str(self.version) + str(self._prev_hash) + str(self._difficulty_target) + str(self._nonce) + str(
            self._timestamp)
        # TODO: Add transactions hash to block hash
        # TODO: Add test to tests/test_block.py
        return gen_hash(data_string)

    def upload_file(self, file_path):
        path = Path(file_path)
        # TODO: Check if mode: r is okay (not rb)
        with open(file_path, mode='r') as new_file:
            new_file = File(new_file.read(), path.name)
            self._files.append(new_file)

    def download_file(self, parent_dir, file_idx):
        file = self._files[file_idx]
        new_path = os.path.join(parent_dir, file.name)
        # TODO: Check if mode: w is okay (not wb)
        with open(new_path, mode='w') as fp:
            fp.write(file.content)

    def is_files_size_valid(self):
        total_size = 0
        for file in self._files:
            total_size += len(file.content.encode(self.STRING_FORMAT))
        if total_size >= self.BLOCK_FILE_SIZE:
            return False
        else:
            return True

    def is_transactions_size_valid(self):
        # TODO: Fix the issue with transaction.content
        total_size = 0
        for transaction in self._transactions:
            total_size += len(transaction.content.encode(self.STRING_FORMAT))
        if total_size >= self.BLOCK_TRANSACTION_SIZE:
            return False

        else:
            return True

    def is_valid(self):
        if (not self._version or not self._prev_hash or not self._difficulty_target or not self._nonce
                or not self._timestamp or not self.is_files_size_valid()
                or not self.is_transactions_size_valid()):
            return False

        else:
            return True

    def save(self, file_path):
        # TODO: Fix the issue with json serialization
        path = os.path.join(file_path, self.FILE_NAME_PREFIX,
                            str(self._timestamp) + self.FILE_EXTENSION)
        json_string = json.dumps(self.to_dict())
        with open(path, mode='w') as file:
            file.write(json_string)
        return path

    def get_files_hash(self):
        files_hash_concat = str()
        for _file in self._files:
            files_hash_concat += _file.hash
        return gen_hash(files_hash_concat)

    def get_transactions_hash(self):
        transactions_hash_concat = str()
        for _transaction in self._transactions:
            transactions_hash_concat += _transaction.get_hash()
        return gen_hash(transactions_hash_concat)

    @staticmethod
    def load(file_path):
        # TODO: Fix the issue with json serialization
        STARTING_INDEX = len(Block.FILE_NAME_PREFIX)
        ENDING_INDEX = -len(Block.FILE_EXTENSION)
        with open(file_path, mode='r') as new_file:
            block_dict = json.loads(new_file.read())
        block_transactions = []
        for transaction in block_dict['transactions']:
            block_transactions.append(Transaction.from_dict(transaction))
        block_files = []
        for file in block_dict['files']:
            block_files.append(File.from_dict(file))
        name = Path(file_path).name
        timestamp = int(name[STARTING_INDEX:ENDING_INDEX])
        return Block(block_dict['version'], block_dict['prev_hash'],
                     block_dict['difficulty_target'], block_dict['nonce'],
                     timestamp, block_transactions, block_files)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return other.version == self._version and other.prev_hash == self._prev_hash \
                   and other.difficulty_target == self._difficulty_target and other.nonce == self._nonce \
                   and other.transactions == self._transactions and other.files == self._files
        return False
