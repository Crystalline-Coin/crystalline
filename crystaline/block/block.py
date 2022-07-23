import os.path

from crystaline.block.helper import gen_hash
from crystaline.file.file import File
from crystaline.transaction.transaction import Transaction
from pathlib import Path
import json
import time

(
    PARAM_VERSION,
    PARAM_PREV_HASH,
    PARAM_DIFF_TARGET,
    PARAM_NONCE,
    PARAM_FILES,
    PARAM_TRANSACTIONS,
    PARAM_TIMESTAMP,
) = (
    "_version",
    "_prev_hash",
    "_difficulty_target",
    "_nonce",
    "_files",
    "_transactions",
    "_timestamp",
)

BLOCK_FILE_SIZE = 3 * 1024 * 1024
BLOCK_TRANSACTION_SIZE = 1 * 1024 * 1024
NONCE_RANGE = (1, 2**20)


class Block:
    FILE_NAME_PREFIX = "cry_"
    FILE_EXTENSION = ".blk"
    STRING_FORMAT = "utf-8"

    def __init__(
        self,
        version: str,
        prev_hash: str,
        difficulty_target: int,
        nonce: int,
        timestamp: time = int(time.time()),
        transactions=None,
        files=None,
    ):
        assert version != None and prev_hash != None and difficulty_target != None and nonce != None and timestamp != None
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
    def version(self) -> str:
        return self._version

    @property
    def prev_hash(self) -> str:
        return self._prev_hash

    @property
    def difficulty_target(self) -> int:
        return self._difficulty_target

    @property
    def nonce(self) -> int:
        return self._nonce

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def transactions(self) -> list:
        return self._transactions

    @property
    def files(self) -> list:
        return self._files

    def to_dict(self):
        block_dict = {
            PARAM_VERSION: self.version,
            PARAM_PREV_HASH: self._prev_hash,
            PARAM_DIFF_TARGET: self._difficulty_target,
            PARAM_NONCE: self._nonce,
            PARAM_TIMESTAMP: self._timestamp,
            PARAM_FILES: self._files,
            PARAM_TRANSACTIONS: self._transactions,
        }
        block_dict[PARAM_TRANSACTIONS] = []
        for transaction in self.transactions:
            block_dict[PARAM_TRANSACTIONS].append(transaction.to_dict())
        block_dict[PARAM_FILES] = []
        for file in self.files:
            block_dict[PARAM_FILES].append(file.to_dict())
        return block_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, block_dict):
        block_transactions = []
        for transaction in block_dict[PARAM_TRANSACTIONS]:
            block_transactions.append(Transaction.from_dict(transaction))
        block_files = []
        for file in block_dict[PARAM_FILES]:
            block_files.append(File.from_dict(file))
        return cls(
            block_dict[PARAM_VERSION],
            block_dict[PARAM_PREV_HASH],
            block_dict[PARAM_DIFF_TARGET],
            block_dict[PARAM_NONCE],
            block_dict[PARAM_TIMESTAMP],
            block_transactions,
            block_files,
        )


    @classmethod
    def from_json(cls, block_json):
        block_dict = json.loads(block_json)
        return cls.from_dict(block_dict)


    def generate_block_hash(self):
        data_string = (
            str(self.version)
            + str(self.prev_hash)
            + str(self.difficulty_target)
            + str(self.nonce)
            + str(self.timestamp)
        )
        # TODO: add transactions hash to block hash
        return gen_hash(data_string)

    def upload_file(self, file_path):
        path = Path(file_path)
        with open(file_path, mode="rb") as new_file:
            file = File(new_file.read(), path.name)
            self._files.append(file)

    def download_file(self, parent_dir, file_idx):
        file = self._files[file_idx]
        new_path = os.path.join(parent_dir, file.name)
        with open(new_path, mode="wb") as fp:
            fp.write(file.content)

    def is_files_size_valid(self):
        total_size = 0
        for file in self._files:
            total_size += file.get_size()
        if total_size >= BLOCK_FILE_SIZE:
            return False
        else:
            return True

    def is_transactions_size_valid(self):
        # TODO: Fix the issue with transaction.content
        total_size = 0
        for transaction in self._transactions:
            total_size += transaction.get_size()
        if total_size >= BLOCK_TRANSACTION_SIZE:
            return False
        else:
            return True

    def is_valid(self):
        if (
            not self.is_nonce_valid()
            or not self.is_files_size_valid()
            or not self.is_transactions_size_valid()
            or not self.is_hash_below_difficulty_target()
            or not type(self.timestamp) == int
        ):
            return False

        else:
            return True

    def is_nonce_valid(self):
        return self._nonce < NONCE_RANGE[1] and self._nonce >= NONCE_RANGE[0]

    def is_hash_below_difficulty_target(self):
        hex_hash = int(self.generate_block_hash(), 16)
        return hex_hash < self._difficulty_target

    def save(self, file_path):
        path = os.path.join(
            file_path,
            self.FILE_NAME_PREFIX + str(self._timestamp) + self.FILE_EXTENSION,
        )
        json_string = self.to_json()
        with open(path, mode="w") as file:
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
        STARTING_INDEX = len(Block.FILE_NAME_PREFIX)
        ENDING_INDEX = -len(Block.FILE_EXTENSION)
        with open(file_path, mode="r") as new_file:
            block_json = new_file.read()
        name = Path(file_path).name
        timestamp = int(name[STARTING_INDEX:ENDING_INDEX])
        return Block.from_json(block_json)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                other.version == self._version
                and other.prev_hash == self._prev_hash
                and other.difficulty_target == self._difficulty_target
                and other.nonce == self._nonce
                and other.transactions == self._transactions
                and other.files == self._files
                and self._timestamp == other.timestamp
            )
        return False
