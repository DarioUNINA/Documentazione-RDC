from socket import *
import subprocess
import os

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) #SOCK_STREAM = TCP
                                            #socket(...) e' il costruttore della classe socket
serverSocket.bind( ('',serverPort) ) #collega la socket al port 1200
                                    #la variabile passata e' una t-pla, indicata con la parentesi tonda e NON e' modificabile
serverSocket.listen(1) #si mette in ascolto, 1 indica la dimensione della coda dei client
print ('The server is ready to receive')


connectionSocket, addr = serverSocket.accept()
print('Accepted a new client', addr)


#script retrieve dati


while True:
    print("prima")
    cmd = connectionSocket.recv(16536).decode()
    print("dopo")
    if cmd.startswith("cd") :
        print("primo if")
        if ((cmd[2:]).isspace() or len(cmd)==2) :
            print("secondo if")
            os.chdir("home")
        else :
            print("else")
            os.chdir(cmd[3:])
        result = os.getcwd()
    else:
        print("secondo else")
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    connectionSocket.send(result.encode())
    

