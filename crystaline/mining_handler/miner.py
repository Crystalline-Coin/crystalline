from crystaline.blockchain.blockchain import Blockchain
from crystaline.block.block import (
    BLOCK_FILE_SIZE,
    BLOCK_TRANSACTION_SIZE,
    NONCE_RANGE,
    Block,
)
import time


class Miner:
    def __init__(
        self, blockchain: Blockchain, file_pool: list, transaction_pool: dict
    ) -> None:
        self.blockchain = blockchain
        self.file_pool = file_pool
        self.transaction_pool = transaction_pool

    def get_items_to_be_mined(self, items, max_items_size):
        items_to_be_mined = []
        items_size = 0

        for item in items:
            items_to_be_mined.append(item)
            items_size += item.get_size()
            if items_size > max_items_size:
                items_to_be_mined.pop(-1)
                break

        return items_to_be_mined

    def mine_block(self):
        files_to_be_mined = self.get_items_to_be_mined(self.file_pool, BLOCK_FILE_SIZE)
        transactions_to_be_mined = self.get_items_to_be_mined(
            self.transaction_pool.values(), BLOCK_TRANSACTION_SIZE
        )

        for i in range(NONCE_RANGE[0], NONCE_RANGE[1]):
            block = Block(
                version="1",
                prev_hash=self.blockchain.get_last_block_hash(),
                difficulty_target=self.blockchain.get_difficulty_target(),
                nonce=i,
                timestamp=int(time.time()),
                transactions=transactions_to_be_mined,
                files=files_to_be_mined,
            )
            if block.is_valid():
                self.blockchain.add_block(block)
                self.file_pool = [
                    x for x in self.file_pool if x not in files_to_be_mined
                ]
                self.transaction_pool = {
                    k: v
                    for k, v in self.transaction_pool.items()
                    if v not in transactions_to_be_mined
                }
                return block
        return None
