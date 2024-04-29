import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce, difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.index) + self.previous_hash + str(self.timestamp) + str(self.transactions) + str(self.nonce) + str(self.difficulty)).encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.difficulty = 0  # Default difficulty target
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.block_generation_time = 10  # Average time to generate a block (assumed to be 10 seconds)
        self.adjustment_interval = 10  # Number of blocks between each difficulty adjustment
        self.start_time = time.time()

    def create_genesis_block(self):
        return Block(1, "0", time.time(), [], 0, self.difficulty)  # Index of the first block is 1

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_block(self, miner_address):
        block = Block(len(self.chain), self.get_latest_block().hash, time.time(), self.pending_transactions, 0, self.difficulty)
        start_time = time.time()
        while not self.is_valid_block(block):
            block.nonce += 1
            block.hash = block.calculate_hash()
        end_time = time.time()
        print(f"| Mined: {block.index} Block | Block hash: {block.hash} | Difficulty: {block.difficulty} | Nonce: {block.nonce} |", end="\r")
        self.chain.append(block)
        self.pending_transactions = [Transaction("network", miner_address, 1)]  # Reward for the miner

        # Check if it's time to adjust the difficulty target
        if len(self.chain) % self.adjustment_interval == 0:
            self.adjust_difficulty()

    def is_valid_block(self, block):
        return block.hash[:block.difficulty] == "0" * block.difficulty

    def adjust_difficulty(self):
        elapsed_time = time.time() - self.start_time
        blocks_generated = len(self.chain)
        expected_blocks = elapsed_time / self.block_generation_time
        ratio = expected_blocks / blocks_generated

        if ratio < 0.9:  # If block generation time is less than 90% of the expected time
            self.difficulty += 1
        elif ratio > 1.1:  # If block generation time is more than 110% of the expected time
            self.difficulty -= 1


class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

# Initialize the blockchain
blockchain = Blockchain()

# Mine new blocks continuously
miner_address = "miner's address"
while True:
    blockchain.mine_block(miner_address)
