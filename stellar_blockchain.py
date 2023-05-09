from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet
from scp import SCPNode
from p2p_network import P2PNetwork

class StellarBlockchain(Blockchain):
    def __init__(self, node: SCPNode):
        super().__init__()
        self.node = node
        self.p2p_network = P2PNetwork()
        self.p2p_network.register_node(node)
        self.wallets = {}
    
    def add_wallet(self, wallet: Wallet):
        self.wallets[wallet.public_key] = wallet

    def create_transaction(self, sender_private_key, recipient_public_key, amount):
        sender_wallet = Wallet(private_key=sender_private_key)
        if sender_wallet.public_key != recipient_public_key:
            transaction = Transaction(sender_wallet.public_key, recipient_public_key, amount)
            if transaction.verify_signature():
                transaction.sign(sender_wallet)
                return transaction
        return None

    def add_transaction(self, transaction: Transaction):
        if transaction.is_valid() and not self.transaction_exists(transaction):
            self.pending_transactions.append(transaction)
            self.node.propose_value(transaction.to_dict())

    def process_block(self, block):
        if block.is_valid(self.chain) and self.node.externalize_value(block.to_dict()):
            self.chain.append(block)
            self.pending_transactions = [transaction for transaction in self.pending_transactions if transaction not in block.transactions]

    def process_pending_transactions(self):
        while self.pending_transactions:
            block = self.create_block(self.pending_transactions[:self.transactions_per_block])
            if block:
                self.process_block(block)
                self.p2p_network.broadcast(self.node, block)
