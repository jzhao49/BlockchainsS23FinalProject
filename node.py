import requests
from blockchain import Blockchain
from transaction import Transaction
from block import Block

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.blockchain = Blockchain()
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def broadcast_transaction(self, transaction):
        for neighbor in self.neighbors:
            url = f'http://{neighbor}/transaction'
            requests.post(url, json=transaction.to_dict())

    def sync_blockchain(self):
        other_chains = []
        for neighbor in self.neighbors:
            url = f'http://{neighbor}/blockchain'
            response = requests.get(url)
            chain = response.json()
            other_chains.append(chain)

        self.blockchain.resolve_conflicts(other_chains)

    def handle_incoming_transaction(self, transaction_data):
        transaction = Transaction(
            sender=transaction_data['sender'],
            receiver=transaction_data['receiver'],
            amount=transaction_data['amount'],
            signature=bytes.fromhex(transaction_data['signature'])
        )

        if self.blockchain.add_transaction(transaction):
            self.broadcast_transaction(transaction)
            return True

        return False

    def handle_incoming_block(self, block_data):
        block = Block(
            index=block_data['index'],
            transactions=[Transaction(**transaction_data) for transaction_data in block_data['transactions']],
            previous_hash=block_data['previous_hash'],
            timestamp=block_data['timestamp'],
            ledger_sequence_number=block_data['ledger_sequence_number']
        )

        return self.blockchain.add_block(block)
