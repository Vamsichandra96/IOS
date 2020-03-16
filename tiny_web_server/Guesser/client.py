import socket
import datetime

x = datetime.datetime.now()
HOST = ''
PORT = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
name = input('enter your name:')
str = 'Hi ' + name
s.send(str.encode())
print(s.recv(1024).decode())
while 1:
    print('enter ready to start the game or break to terminate the game')
    temp = input().lower()
    if(temp == 'ready'):
        s.send(b'ready')
        break
    elif(temp == 'break'):
        s.send(b'break')
        exit()

while 1:
    try:
        print('Enter the number from 1 to 100:')
        userInput = input()
        temp = int(userInput)
        s.send(userInput.encode())
        serverOutput = s.recv(1024).decode()
        print(serverOutput)
        if("Correct" in serverOutput):
            
            break
    except :
        print('only numbers are expected')
        pass
    
s.close()