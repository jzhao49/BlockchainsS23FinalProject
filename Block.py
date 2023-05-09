import json
import time
from hashlib import sha256 as H

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None, ledger_sequence_number=None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or int(time.time())
        self.ledger_seq_number = ledger_sequence_number

    def hash(self):
        block_data = {
            'index': self.index,
            'transactions': [transaction.__dict__ for transaction in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }
        block_json = json.dumps(block_data, sort_keys=True).encode()
        block_hash = H(block_json).hexdigest()
        return block_hash
    
    @classmethod
    def create_genesis_block(cls):
        return cls(index = 0, transactions=[], previous_hash="0")
