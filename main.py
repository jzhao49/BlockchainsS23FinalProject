import time
from stellar_blockchain import StellarBlockchain
from scp import SCPNode
from wallet import Wallet
from p2p_network import P2PNetwork
from transaction import Transaction

# Initialize SCP nodes
nodes = [
    SCPNode("Node1", threshold=2),
    SCPNode("Node2", threshold=2),
    SCPNode("Node3", threshold=2),
    SCPNode("Node4", threshold=2),
]

# Define quorum slices
for node in nodes:
    node.add_validator_set(nodes)

# Initialize P2P network
p2p_network = P2PNetwork()

# Register SCP nodes in the P2P network
for node in nodes:
    p2p_network.register_node(node)

# Initialize Stellar blockchain with the first node as the main node
stellar_blockchain = StellarBlockchain(nodes[0])

# Create wallets and a sample transaction
wallet1 = Wallet()
wallet2 = Wallet()
stellar_blockchain.add_wallet(wallet1)
stellar_blockchain.add_wallet(wallet2)

transaction = stellar_blockchain.create_transaction(wallet1.private_key, wallet2.public_key, 10)

# Add transaction to the Stellar blockchain
stellar_blockchain.add_transaction(transaction)

# Simulate SCP protocol and measure the time taken for consensus
start_time = time.time()

# Nodes receive messages from the P2P network and process them
while any(node.state != SCPNode.State.EXTERNALIZED for node in nodes):
    for node in nodes:
        messages = p2p_network.receive(node)
        for message in messages:
            node.process_message(message)

elapsed_time = time.time() - start_time
print(f"Time taken for consensus: {elapsed_time:.2f} seconds")
