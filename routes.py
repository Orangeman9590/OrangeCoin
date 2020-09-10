import sys
from blockchain import Blockchain, Transaction, Block
import pprint
from login import Login
import time
import os
import os.path
from flask import Flask, jsonify, request, flash
from uuid import uuid4
from argparse import ArgumentParser
pp = pprint.PrettyPrinter(indent=4)



login = Login(key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e')
print('Creating OrangeCoin Blockchain...')
blockchain = Blockchain()
print(blockchain)
print('Generating Key Pair...')
key = blockchain.generate_keys()
print(key)
node_address = uuid4().hex



app = Flask(__name__)

@app.route('/create-transaction', methods=['POST'])
def create_transaction():
    sender = input('Who are you: ')
    reciever = input('Who Would You Like To Send To: ')
    amount = input('How Much OrangeCoin are you Sending: ')

    index = blockchain.add_transaction(sender=sender, reciever=reciever,amount=amount,key_string=key,sender_key=key)
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201



@app.route('/mine', methods=['GET'])
def mine() :
    block = blockchain.mine_pending_transactions(node_address)
    response = {'chain' : blockchain.chainJSONencode()}
    return jsonify(response)


@app.route('/chain', methods=['GET'])
def get_full_chain() :
    response = {'chain':blockchain.chainJSONencode()}
    return jsonify(response)

@app.route('/register-node', methods=['POST'])
def register_nodes():
    nodes = input('What address would you like to register as a node: ')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400


    blockchain.register_node(nodes)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/sync-chain', methods=['GET'])
def consensus() :
    blockchain.get_neighbour_chains()
