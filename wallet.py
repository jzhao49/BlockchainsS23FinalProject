import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class Wallet:
    def __init__(self, private_key=None, public_key=None):
        if private_key and public_key:
            self.private_key = private_key
            self.public_key = public_key
        else:
            self.private_key, self.public_key = self.generate_key_pair()

    @staticmethod
    def generate_key_pair():
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        return (
            private_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            ),
            public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
        )

    def sign_transaction(self, transaction):
        transaction.sign(self.private_key)

    @staticmethod
    def verify_transaction(transaction):
        return transaction.verify_signature()