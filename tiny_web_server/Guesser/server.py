'''
    Write a python server program that
        0. initialized a socket connection on localhost and port 10000
        1. accepts a connection from a  client
        2. receives a "Hi <name>" message from the client
        3. generates a random numbers and keeps it a secret
        4. sends a message "READY" to the client
        5. waits for the client to send a guess
        6. checks if the number is
            6.1 equal to the secret then it should send a message "Correct! <name> took X attempts to guess the secret"
            6.2 send a message "HIGH" if the guess is greater than the secret
            6.3 send a message "LOW" if the guess is lower than the secrent
        7. closes the client connection and waits for the next one
'''


import socket
import random
HOST = ''
PORT = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()

def checkNumber():
    global chances
    global status
    temp1 = conn.recv(1024)
    temp2 = temp1.decode("utf8")
    temp = int(temp2)
    if(temp > secretNumber):
        conn.send(b'HIGH')
    elif(temp < secretNumber):
        conn.send(b'LOW')
    else:
        str = "Correct! %s took %s attempts to guess the secret" %(playerName,chances)
        conn.send(str.encode())
        status = False
        return
    chances += 1
    print("chances: ", chances)

chances = 0
status = True
playerName =""
while 1:
    conn,addr = s.accept()
    print('connected by' ,addr)
    data = conn.recv(1024)
    dataArray = data.split()
    playerName = dataArray[1]
    conn.send(b'READY')
    secretNumber = random.randint(1,100)
    status = True
    chances = 0
    while status:
        checkNumber()
    conn.close()