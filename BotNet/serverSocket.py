from socket import *
import subprocess

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) #SOCK_STREAM = TCP
                                            #socket(...) e' il costruttore della classe socket
serverSocket.bind( ('',serverPort) ) #collega la socket al port 1200
                                    #la variabile passata e' una t-pla, indicata con la parentesi tonda e NON e' modificabile
serverSocket.listen(1) #si mette in ascolto, 1 indica la dimensione della coda dei client
print ('The server is ready to receive')


connectionSocket, addr = serverSocket.accept()
print('Accepted a new client', addr)

while True:
    comando = connectionSocket.recv(16536).decode()
    result = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    connectionSocket.send(result.stdout.encode())    