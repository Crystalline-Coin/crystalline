from crystaline.blockchain.blockchain import Blockchain
from crystaline.file.file import File


class Miner:
    def __init__(self, blockchain:Blockchain, file_pool, transaction_pool) -> None:
        self.blockchain = blockchain
        self.file_pool = file_pool
        self.transaction_pool = transaction_pool
    
    def mine_block(self):
        files_to_be_mined = []
        files_size = 0
        transactions_to_be_mined = []

        for file in self.file_pool:
            files_to_be_mined.append(file)
            files_size += File(file).size