from socket import *
import os

serverName = '192.168.136.118' #e' un nome simbolico, che il DNS (un sistema interno) che lo traduce in IP
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
while True:
    sentence = input('Input lowercase sentence:')
    clientSocket.send(sentence.encode())
    modfiedSentence = clientSocket.recv(1024)
    print('From Server:', modfiedSentence.decode())
clientSocket.close()    