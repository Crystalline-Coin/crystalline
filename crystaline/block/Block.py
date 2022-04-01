from pathlib import Path
import json
import time

from ..block.helper import gen_hash
from ..file.file import File
from ..transaction.Transaction import Transaction

FILE_NAME_PREFIX = "cry_"
FILE_EXTENSION = ".blk"
BLOCK_FILE_SIZE = 3 * 1024 * 1024
BLOCK_TRANSACTION_SIZE = 1 * 1024 * 1024
STRING_FORMAT = "utf-8"


class Block:
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
        self.version = version
        self.prev_hash = prev_hash
        self.difficulty_target = difficulty_target
        self.nonce = nonce
        self.timestamp = timestamp
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = list(transactions)
        if files is None:
            self.files = []
        else:
            self.files = list(files)
        if transactions is None:
            self.transactions = []
        else:
            self.transactions = list(transactions)

    def to_dict(self):
        block_dict = {
            "version": self.version,
            "prev_hash": self.prev_hash,
            "difficulty_target": self.difficulty_target,
            "nonce": self.nonce,
        }
        block_dict["transactions"] = []
        for transaction in self.transactions:
            block_dict["transactions"].append(transaction.to_dict())
        block_dict["files"] = []
        for file in self.files:
            block_dict["files"].append(file.to_dict())
        return block_dict

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
            new_file = File(new_file.read(), path.name)
            self.files.append(new_file)

    def download_file(self, file_path, file_index):
        file = self.files[file_index]
        new_path = file_path + "/" + file.name
        with open(new_path, mode="wb") as new_file:
            new_file.write(file.content)

    def is_file_size_valid(self):
        total_size = 0
        for file in self.files:
            total_size += len(file.content.encode(STRING_FORMAT))
        if total_size >= BLOCK_FILE_SIZE:
            return False

        else:
            return True

    def is_transaction_size_valid(self):
        total_size = 0
        for transaction in self.transactions:
            total_size += len(transaction.content.encode(STRING_FORMAT))
        if total_size >= BLOCK_TRANSACTION_SIZE:
            return False

        else:
            return True

    def is_valid(self, files_dir, transactions_dir):
        if (
            not self.version
            or not self.prev_hash
            or not self.difficulty_target
            or not self.nonce
            or not self.timestamp
            or not self.is_file_size_valid(files_dir)
            or not self.is_transaction_size_valid(transactions_dir)
        ):
            return False

        else:
            return True

    def save(self, file_path):
        block_dict = self.to_dict()
        path = file_path + "/" + FILE_NAME_PREFIX + str(self.timestamp) + FILE_EXTENSION
        json_string = json.dumps(block_dict)
        with open(path, mode="w") as file:
            file.write(json_string)

    def get_files_hash(self):
        files_hash_concat = str
        for _file in self.files:
            files_hash_concat += _file.file_hash
        return gen_hash(files_hash_concat)

    def get_transactions_hash(self):
        transactions_hash_concat = str
        for _transaction in self.transactions:
            transactions_hash_concat += _transaction.get_hash()
        return gen_hash(transactions_hash_concat)

    @staticmethod
    def load(file_path):
        STARTING_INDEX = len(FILE_NAME_PREFIX)
        ENDING_INDEX = -len(FILE_EXTENSION)
        with open(file_path, mode="r") as new_file:
            block_dict = json.loads(new_file.read())
        block_transactions = []
        for transaction in block_dict["transactions"]:
            block_transactions.append(Transaction.from_dict(transaction))
        block_files = []
        for file in block_dict["files"]:
            block_files.append(File.from_dict(file))
        name = Path(file_path).name
        timestamp = int(name[STARTING_INDEX:ENDING_INDEX])
        return Block(
            block_dict["version"],
            block_dict["prev_hash"],
            block_dict["difficulty_target"],
            block_dict["nonce"],
            timestamp,
            block_transactions,
            block_files,
        )
