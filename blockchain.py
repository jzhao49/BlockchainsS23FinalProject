import time
from block import Block
from transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain = [Block.create_genesis_block()]
        self.pending_transactions = []

    def add_block(self, block: Block):
        if self.is_valid_new_block(block):
            self.chain.append(block)
            return True
        return False

    def add_transaction(self, transaction: Transaction):
        if transaction.verify_signature():
            self.pending_transactions.append(transaction)
            return True
        return False
    
    def create_new_block(self, ledger_sequence_number: int):
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.last_block().hash(),
            ledger_sequence_number=ledger_sequence_number
        )
        self.pending_transactions = []
        return new_block

    def is_valid_new_block(self, new_block: Block):
        if new_block.previous_hash != self.last_block().hash():
            return False
        
        for transaction in new_block.transactions:
            if not transaction.verify_signature():
                return False
            
        return True

    def is_valid_chain(self, chain):
        for i in range(1, len(chain)):
            if not self.is_valid_new_block(chain[i]):
                return False
            if chain[i].previous_hash != chain[i-1].hash():
                return False
        
        return True

    def resolve_conflicts(self, other_chains):
        longest_chain = self.chain
        for chain in other_chains:
            if len(chain) > len(longest_chain) and self.is_valid_chain(chain):
                longest_chain = chain
        
        if longest_chain != self.chain:
            self.chain = longest_chain
            return True
        
        return False

    def last_block(self):
        return self.chain[-1]