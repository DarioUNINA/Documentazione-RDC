from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) #SOCK_STREAM = TCP
                                            #socket(...) e' il costruttore della classe socket
serverSocket.bind( ('',serverPort) ) #collega la socket al port 1200
                                    #la variabile passata e' una t-pla, indicata con la parentesi tonda e NON e' modificabile
serverSocket.listen(1) #si mette in ascolto, 1 indica la dimensione della coda dei client
print ('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    print('Accepted a new client', addr)
    sentence = connectionSocket.recv(1024).decode() #1024 e' il numero max di byte da ricevere, decode serve per rendere il codice indipendente dall' architettura
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()