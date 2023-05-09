import json
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature
    
    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'signature': self.signature.hex() if self.signature else None
        }

    def serialize(self):
        transaction_data = {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount
        }
        return json.dumps(transaction_data, sort_keys=True).encode()

    def sign(self, private_key):
        private_key_object = ed25519.Ed25519PrivateKey.from_private_bytes(private_key)
        self.signature = private_key_object.sign(self.serialize())

    def verify_signature(self):
        # Genesis transaction
        if self.sender == "0": 
            return True

        public_key_bytes = self.sender
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)
        try:
            public_key.verify(self.signature, self.serialize())
            return True
        except Exception:
            return False

    def __repr__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"

