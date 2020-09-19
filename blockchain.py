import hashlib
import json
from textwrap import dedent
from uuid import uuid4
import jsonpickle
import flask
from flask import Flask, url_for
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
from Crypto.Signature import *
from datetime import datetime
import requests





class Block(object) :
    def __init__(self, transactions, time, index) :
        self.index = index
        self.transactions = transactions
        self.time = time
        self.prev = ''
        self.nonce = 0
        self.orange = self.calculate_orange()
        self.hash = self.calculate_hash()

    def calculate_orange(self):
        return '24 hr'

    def calculate_hash(self):
        hash_transactions = ''
        for transaction in self.transactions:
            hash_transactions += transaction.hash
        hash_string = str(self.time) + hash_transactions + self.orange + self.prev + str(self.nonce)
        hash_encoded = json.dumps(hash_string, sort_keys=True).encode()
        return hashlib.sha256(hash_encoded).hexdigest()
    def mine_block(self, difficulty):
        arr = []
        for i in range(0, difficulty):
            arr.append(i)

        arr_str = map(str, arr)
        hash_puzzle = ''.join(arr_str)
        while self.hash[0:difficulty] != hash_puzzle:
            self.nonce +=1
            self.hash = self.calculate_hash()
            print('Nonce:', self.nonce)
            print('Hash Attempt:', self.hash)
            print('Hash We Want:', hash_puzzle, '...')
            print('')


        print('Block Mined, Proof of Work:', self.nonce)
        return True

    def hash_valid_transactions(self):
        for i in range(0, len(self.transactions)):
            transaction = self.transactions[i]
            if not transaction.is_valid_transaction():
                return False
            return True

    def JSON_encode(self):
        return jsonpickle.encode(self)


class Blockchain(object):
    def __init__(self):
        self.chain = [self.add_genesis_block()]
        self.pendingTransactions = []
        self.difficulty = 3
        self.mineReward = 100
        self.blockSize = 10
        self.nodes = set()




    def register_node(self, address):
        self.nodes.add(address)
        return True

    def get_neighbour_chains(self) :
        neighbour_chains = []
        newChain = None


        for node_address in self.nodes :
            resp = requests.get(node_address+'/chain').json()

            max_length = len(self.chain)
            chain = resp['chain']
            neighbour_chains.append(chain)
            longest_chain = max(neighbour_chains, key=len)
            print(neighbour_chains)

            if max_length >= len(longest_chain):
                response = {
                    'message' : 'Chain is already up to date',
                    'chain' : self.chainJSONencode()
                }
                return flask.jsonify(response)
            else :
                max_length = longest_chain
                newChain = chain
                print(self.chainJSONdecode(newChain))

                if newChain :
                    self.chain = self.chainJSONdecode(newChain)
                    return self.chain
            return False


    def mine_pending_transactions(self, miner):
        len_pt = len(self.pendingTransactions)
        if (len_pt <= 1) :
            print("Not enough transactions to mine! (Must be > 1)")
            return False;
        for i in range(0, len_pt, self.blockSize):
            end = i + self.blockSize
            if i >= len_pt:
                end = len_pt

            transaction_slice = self.pendingTransactions[i:end]
            new_block = Block(transaction_slice, datetime.now().strftime('%m/%d/%Y, %H:%M:%S'), len(self.chain))
            hash_val = self.get_last_block().hash
            new_block.prev = hash_val
            new_block.mine_block(self.difficulty)
            self.chain.append(new_block)
        print('Mining Transactions Complete')
        pay_miner = Transaction("Miner Reward", miner, self.mineReward)
        self.pendingTransactions = [pay_miner]
        return True

    def get_balance(self, person):
        balance = 100
        lenPT = len(self.pendingTransactions)
        if (lenPT <= 1) :
            print("Not enough transactions to mine! (Must be > 1)")
            return False
        else :
            for i in range(1, len(self.chain)):
                block = self.chain[i]
                try:
                    for j in range(0, len(block.transactions)):
                        transaction = block.transactions[j]
                        if(transaction.sender == person):
                            balance -= int(transaction.amount)
                            print(balance)
                        if transaction.reciever == person:
                            balance += int(transaction.amount)
                            print(balance)
                except AttributeError:
                    print('No Transaction')
            return balance + 100


    def add_transaction(self, sender, reciever, amount, key_string, sender_key):
        key_byte = key_string.encode('ASCII')
        sender_key_byte = sender_key.encode('ASCII')

        key = RSA.import_key(key_byte)
        sender_key = RSA.import_key(sender_key_byte)

        if not sender or not reciever or not amount:
            print('transaction error 1')
            return False
        transaction = Transaction(sender, reciever, amount)
        transaction.sign_transaction(key, sender_key)
        self.pendingTransactions.append(transaction)
        return len(self.chain) + 1



    def get_last_block(self):
        return self.chain[-1]

    def add_genesis_block(self):
        t_arr = []
        t_arr.append(Transaction("me", 'you', 10))
        genesis = Block(t_arr, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0)
        genesis.prev = 'None'
        return genesis

    def isValidChain(self) :
        for i in range(1, len(self.chain)) :
            b1 = self.chain[i - 1]
            b2 = self.chain[i]
            if not b2.hash_valid_transactions() :
                print("error 3")
                return False
            if b2.hash != b2.calculate_hash() :
                print("error 4")
                return False
            if b2.prev != b1.hash :
                print("error 5")
                return False
        return True

    def generate_keys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        file_out = open('private.pem', 'wb')
        file_out.write(private_key)

        public_key = key.publickey().export_key()
        file_out = open('receiver.pem', 'wb')
        file_out.write(public_key)

        return key.publickey().export_key().decode('ASCII')

    def chainJSONencode(self) :

        blockArrJSON = []
        for block in self.chain :
            blockJSON = {}
            blockJSON['hash'] = block.hash
            blockJSON['index'] = block.index
            blockJSON['prev'] = block.prev
            blockJSON['time'] = block.time
            blockJSON['nonce'] = block.nonce
            blockJSON['orange'] = block.orange
            blockJSON['length'] = int(len(self.chain))

            transactionsJSON = []
            tJSON = {}
            for transaction in block.transactions :
                tJSON['time'] = transaction.time
                tJSON['sender'] = transaction.sender
                tJSON['reciever'] = transaction.reciever
                tJSON['amount'] = transaction.amount
                tJSON['hash'] = transaction.hash
                transactionsJSON.append(tJSON)

            blockJSON['transactions'] = transactionsJSON

            blockArrJSON.append(blockJSON)

        return blockArrJSON

    def chainJSONdecode(self, chainJSON) :
        chain = []
        for blockJSON in chainJSON :

            tArr = [];
            for tJSON in blockJSON['transactions'] :
                transaction = Transaction(tJSON['sender'], tJSON['reciever'], tJSON['amount'])
                transaction.time = tJSON['time']
                transaction.hash = tJSON['hash']
                tArr.append(transaction)

            block = Block(tArr, blockJSON['time'], blockJSON['index'])
            block.hash = blockJSON['hash']
            block.prev = blockJSON['prev']
            block.nonce = blockJSON['nonce']
            block.orange = blockJSON['orange']

            chain.append(block);
        return chain;

    def get_block_object_from_block_data(self, block_data):
        return Block(
            block_data['index'],
            block_data['prev'],
            block_data['transactions'])






class Transaction(object) :
    def __init__(self, sender, reciever, amount) :
        self.sender = sender
        self.reciever = reciever
        self.amount = amount
        self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.hash = self.calculate_hash()

    def calculate_hash(self) :
        hashString = self.sender + self.reciever + str(self.amount) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()

    def is_valid_transaction(self):
        if self.hash != self.calculate_hash():
            print('1')
            return False
        if self.sender == self.reciever:
            print('2')
            return False
        if self.sender == "Miner Rewards":
            print('3')
            return True
        if not self.signature or len(self.signature) == 0:
            print("No Signature")
            return False

    def sign_transaction(self, key, sender_key):
        if self.hash != self.calculate_hash():
            print('Transaction Tampered Error')
            return False
        if str(key.publickey().export_key()) != str(sender_key.publickey().export_key()):
            print('Transaction attempt to be signed from another wallet')
            return False
        pkcs1_15.new(key)
        self.signature = 'made'
        print('Made Signature')
        return True

