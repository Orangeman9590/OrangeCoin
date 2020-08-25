import sys
from blockchain import Blockchain, Transaction, Block
import pprint
from login import Login
import time
import os
import os.path
pp = pprint.PrettyPrinter(indent=4)


orangecoin_graphic = '''
 _____                                      _       
|  _  |                                    (_)      
| | | |_ __ __ _ _ __   __ _  ___  ___ ___  _ _ __  
| | | | '__/ _` | '_ \ / _` |/ _ \/ __/ _ \| | '_ \ 
\ \_/ / | | (_| | | | | (_| |  __/ (_| (_) | | | | |
 \___/|_|  \__,_|_| |_|\__, |\___|\___\___/|_|_| |_|
                        __/ |                       
                       |___/                        
+++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


login = Login(key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e')
blockchain = Blockchain()


if os.path.isfile('data.txt.enc') and os.path.isfile('data2.txt.enc') :
    while True :
        os.system('cls')
        username = str(input('Enter Username: '))
        password = str(input("Enter password: "))
        login.decrypt_file('data2.txt.enc')
        login.decrypt_file("data.txt.enc")
        p = ''
        with open("data.txt", "r") as f :
            p = f.readlines()
        with open('data2.txt', 'r') as g :
            u = g.readlines()
        if p[0] == password and u[0] == username :
            login.encrypt_file("data.txt")
            login.encrypt_file("data2.txt")
            print('Welcome ' + username)
            sender = username
            break
        elif p[0] == password and u[0] != username :
            login.encrypt_file("data.txt")
            login.encrypt_file("data2.txt")
            print('Invalid username')
            sys.exit(1)
        elif p[0] != password and u[0] == username :
            login.encrypt_file("data.txt")
            login.encrypt_file("data2.txt")
            print('Invalid password')
            sys.exit(1)
        elif p[0] != password and u[0] != username :
            login.encrypt_file("data.txt")
            login.encrypt_file("data2.txt")
            print('Invalid username and password')
            sys.exit(1)

    key = blockchain.generate_keys()
    print(key)
    while True:
        os.system('cls')
        print(orangecoin_graphic)
        print('1. Send OrangeCoin')
        print('2. Mine Pending Transactions')
        print('3. Check Blockchain')
        print('99. Exit')
        choice = input('> ')
        if choice == '1':
            os.system('cls')
            reciever = input('Who Would You Like To Send To: ')
            amount = input('How Much OrangeCoin are you Sending: ')
            transaction = Transaction(sender, reciever, amount)
            blockchain.pendingTransactions.append(transaction)
            print(blockchain.pendingTransactions)
            print('Sent!')
            print('PRESS ENTER TO GO BACK')
            yi = input()
        if choice == '2':
            os.system('cls')
            miner = sender
            blockchain.mine_pending_transactions(miner)
            blockchain.mine_pending_transactions(miner)
            print('')
            print('=============================================B-L-O-C-K-C-H-A-I-N==========================================')
            pp.pprint(blockchain.chainJSONencode())
            print('Length: ', len(blockchain.chain))
            blockchain.get_balance(miner)
            print('PRESS ENTER TO GO BACK')
            yi = input()
        if choice == '3':
            os.system('cls')
            pp.pprint(blockchain.chainJSONencode())
            print('Length: ', len(blockchain.chain))
            print('PRESS ENTER TO GO BACK')
            yi = input()
        if choice == '99':
            sys.exit(1)







else :
    while True :
        os.system('cls')
        username = str(input("Enter a Username: "))
        password = str(input("Setting up stuff. Enter a password that will be used for decryption: "))
        repassword = str(input("Confirm password: "))
        if password == repassword :
            break
        else :
            print("Passwords Mismatched!")
    print("__________________________________________________")
    print("|                                                 |")
    print("|                   WELCOME                       |")
    print("|                     TO                          |")
    print("|                 ORANGECOIN                      |")
    print("|                                                 |")
    print(" _________________________________________________")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    login.encrypt_file("data.txt")
    g = open('data2.txt', 'w+')
    g.write(username)
    g.close()
    login.encrypt_file('data2.txt')
    print("Please restart the program to complete the setup")
    time.sleep(15)
