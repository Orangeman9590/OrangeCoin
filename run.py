import sys
from blockchain import Blockchain, Transaction, Block
import pprint

pp = pprint.PrettyPrinter(indent=4)

blockchain = Blockchain()

key = blockchain.generate_keys()
print(key)
print('')

sender = input('Who Are You: ')
reciever = input('Who Would You Like To Send To: ')
amount = input('How Much OrangeCoin are you Sending: ')
transaction = Transaction(sender, reciever, amount)


blockchain.pendingTransactions.append(transaction)
print(blockchain.pendingTransactions)
mine = input('Would You Like To mine pending transactions[y/n]:')
if mine == 'y':
    blockchain.mine_pending_transactions('Erik')
    print('===========BLOCKCHAIN============')
    print(blockchain.chain)
elif mine == 'n':
    print(blockchain.chain)
    sys.exit(1)

pp.pprint(blockchain.chainJSONencode())
print('Length: ', len(blockchain.chain))