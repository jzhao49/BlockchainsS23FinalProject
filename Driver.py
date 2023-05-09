import random
from typing import List
from transaction import Transaction
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from BallotProtocol import SCPNode


def generate_key_pair():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

def deserialize_public_key(pem_public_key):
    return serialization.load_pem_public_key(
        pem_public_key.encode('utf-8')
    )

def sign_transaction(transaction, private_key):
    return private_key.sign(transaction.__str__().encode('utf-8'))

def verify_transaction_signature(transaction, public_key):
    try:
        public_key.verify(transaction.signature, transaction.__str__().encode('utf-8'))
        return True
    except InvalidSignature:
        return False

def generate_transactions(num_transactions: int) -> List[Transaction]:
    transactions = []
    for _ in range(num_transactions):
        sender_public_key = "Sender-" + str(random.randint(1, 100))
        receiver_public_key = "Receiver-" + str(random.randint(1, 100))
        amount = random.randint(1, 100)
        transactions.append(Transaction(sender_public_key, receiver_public_key, amount))
    return transactions

def main():
    # Generate key pairs for nodes
    key_pairs = [generate_key_pair() for _ in range(5)]

    # Create nodes and quorum slices
    nodes = [SCPNode(private_key, public_key) for private_key, public_key in key_pairs]
    for node in nodes:
        node.known_nodes = set(nodes) - {node}
        node.add_quorum_slice(nodes)

    # Generate transactions
    transactions = generate_transactions(10)

    # Run SCP
    for i, transaction in enumerate(transactions):
        nominating_node = nodes[i % len(nodes)]
        nominating_node.nominate(transaction)
        nominating_node.start_ballot_protocol(i + 1)

    # Print final ledgers
    for i, node in enumerate(nodes):
        print(f"Node {i + 1} ledger:")
        for transaction in node.ledger.transactions:
            print(transaction)

if __name__ == "__main__":
    main()
