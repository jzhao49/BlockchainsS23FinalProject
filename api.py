from flask import Flask, request, jsonify
from stellar_blockchain import StellarBlockchain
from wallet import Wallet
from p2p_network import P2PNetwork

app = Flask(__name__)
stellar_blockchain = StellarBlockchain()
p2p_network = P2PNetwork()

@app.route('/wallet', methods=['POST'])
def create_wallet():
    wallet = Wallet()
    stellar_blockchain.add_wallet(wallet)
    response = {
        'public_key': wallet.public_key,
        'private_key': wallet.private_key
    }
    return jsonify(response), 201

@app.route('/wallet/<public_key>/balance', methods=['GET'])
def get_balance(public_key):
    balance = stellar_blockchain.get_balance(public_key)
    if balance is not None:
        response = {
            'public_key': public_key,
            'balance': balance
        }
        return jsonify(response), 200
    else:
        response = {
            'error': 'Wallet not found'
        }
        return jsonify(response), 404

@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    sender_private_key = data['sender_private_key']
    recipient_public_key = data['recipient_public_key']
    amount = data['amount']

    transaction = stellar_blockchain.create_transaction(sender_private_key, recipient_public_key, amount)
    if transaction:
        stellar_blockchain.add_transaction(transaction)
        p2p_network.broadcast(stellar_blockchain.node, transaction)
        response = {
            'transaction': transaction.to_dict()
        }
        return jsonify(response), 201
    else:
        response = {
            'error': 'Invalid transaction'
        }
        return jsonify(response), 400

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = [transaction.to_dict() for transaction in stellar_blockchain.pending_transactions]
    return jsonify(transactions), 200

if __name__ == '__main__':
    app.run(debug=True)
