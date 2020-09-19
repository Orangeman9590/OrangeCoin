import pprint
from argparse import ArgumentParser
from routes import app
import os
from login import Login
import time
import sys
import requests
pp = pprint.PrettyPrinter(indent=4)

port = input('What port would you like to run on: ')
os.system('start cmd /c python runhost.py -p ' + port)
time.sleep(50)
clear = lambda: os.system('cls')


def register_node(node_addr, parent_server) :
    requests.post(parent_server + '/register-node', json={'address' : node_addr})
    print("\\nOn Server {}: Node-{} has been registered successfully!\\n".format(parent_server, node_addr))


def create_transaction(server, data) :
    requests.post(server + '/create-transaction', json=data).json()
    print("On Server {}: Transaction has been processed!\\n".format(server))


def mine_block(server) :
    print('Mining Pending Transactions...')
    requests.get(server + '/mine').json()
    print("On Server {}: Block has been mined successfully!\\n".format(server))


def get_server_chain(server) :
    resp = requests.get(server + '/chain').json()
    print("On Server {}: Chain is-\\n{}\\n".format(server, resp))
    return resp


def sync_chain(server) :
    print("On Server {}: Started Syncing Chain . . .".format(server))
    resp = requests.get(server + '/sync-chain')
    print("On Server {}: Chain synced!\\n".format(server))

own_server = f'http://127.0.0.1:{port}'
server1 = 'http://127.0.0.1:5000'
register_node(server1, own_server)

while True:
    os.system('cls')
    print('1. Send OrangeCoin')
    print('2. Mine Pending Transactions')
    print('3. Check Blockchain')
    print('4. Sync Chain')
    print('5. Register Node')
    print('99. Exit')
    choice = input('> ')
    if choice == '1':
        os.system('cls')
        sender = input('Who are you: ')
        reciever = input('Who Would You Like To Send To: ')
        amount = int(input('How Much OrangeCoin are you Sending: '))
        create_transaction(own_server, {'sender':sender, 'reciever':reciever,'amount':amount})
        print('PRESS ENTER TO GO BACK')
        yi = input()
    if choice == '2':
        os.system('cls')
        mine_block(own_server)
        print('')
        print('=============================================B-L-O-C-K-C-H-A-I-N==========================================')
        pp.pprint(get_server_chain(own_server))
        print('Length: ', len(get_server_chain(own_server)))
        print('PRESS ENTER TO GO BACK')
        yi = input()
    if choice == '3':
        os.system('cls')
        pp.pprint(get_server_chain(own_server))
        print('Length: ', len(get_server_chain(own_server)))
        print('PRESS ENTER TO GO BACK')
        yi = input()
    if choice == '4':
        sync_chain(own_server)
    if choice == '5':
        node = input('What address would you like to register as a node: ')
        register_node(node, own_server)
    if choice == '99':
        sys.exit(1)

