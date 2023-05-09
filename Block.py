import time
import hashlib
# from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
# from cryptography.hazmat.primitives import serialization
# from cryptography.exceptions import InvalidSignature

class Block:
    def __init__(self, txns, prev):
        self.txns = txns
        self.prev = prev
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_data = "".join[(
            str(tx) for tx in self.txns
        )] + str(self.timestamp) + str(self.nonce) + str(self.prev)

        block_hash = hashlib.sha256(block_data.encode('utf-8')).hexdigest()

        return block_hash

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" + difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def __repr__(self):
        return f"Block: {self.hash} (previous: {self.prev})"
