from transaction import Transaction
from block import Block

class Ledger:
    def __init__(self):
        self.blocks = [self.create_genesis_block()]

    def create_genesis_block(self):
        genesis_tx = Transaction("genesis", "genesis", 0)
        return Block([genesis_tx], "0")

    def add_block(self, txns):
        prev = self.blocks[-1].hash
        new_block = Block(txns, prev)
        self.blocks.append(new_block)
    
    def validate_chain(self):
        for i in range(1, len(self.blocks)):
            cur_block = self.blocks[i]
            prev_block = self.blocks[i - 1]

            if cur_block.hash != cur_block.calculate_hash():
                return False
            if cur_block.prev != prev_block.hash:
                return False
        return True