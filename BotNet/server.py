from socket import *
import os
import sys
import time



def connection():

    while True:

        ip = input("Inserisci indirizzo IP: ")
   
        try:

            serverName = ip #e' un nome simbolico, che il DNS (un sistema interno) che lo traduce in IP
            serverPort = 11926
            serverSocket = socket(AF_INET, SOCK_STREAM)
            serverSocket.connect((serverName,serverPort))

        except ConnectionRefusedError:

            print("Errore di connessione\n")
            time.sleep(2)

        else:

            print("Connessione effettuata correttamente")
            return serverSocket



def printOptions():

    print("\nQuale operazione vuoi svolgere?\n")
    print("1) Comando da terminale\n")
    print("2) Esci\n")



def setup(serverSocket):

    file = open(os.path.join(sys.path[0], 'dati.txt'), mode='a', encoding='latin-1')
    
    result = (str)(serverSocket.recv(1048576).decode(encoding='latin-1'))

    while not(result.endswith("uscita")):
        file.write("\n******************************************\n\n"+result)
        result = (str)(serverSocket.recv(1048576).decode(encoding='latin-1'))
    
    file.write("\n******************************************\n\n"+result.rstrip('uscita'))
            
    file.close()
    
    


def shell(serverSocket):

    print("Inserisci i comandi che vuoi eseguire da terminale\n(esc per uscire , print per salvare l'ultimo output, erase per eliminare i dati salvati)\n ")
    result = ''
        
    while True:

        file = open(os.path.join(sys.path[0], 'dati.txt'), mode='a', encoding='latin-1')
        comando = input('inserisci comando: ')
        
        if comando == "esc":
            file.close()
            break
        
        elif comando == "print": #scrive sul file l'ultimo output (lo crea se non esiste)
            file.write("\n******************************************\n\n"+result)
            continue

        elif comando == "erase": #cancella il contenuto del file (lo crea se non esiste)
            file.truncate(0)
            continue

        elif comando == "" or comando.isspace():
            print("\ncomando non valido\n")
            continue
        
        else:
            serverSocket.send(comando.encode(encoding='latin-1'))
            result = serverSocket.recv(1048576).decode(encoding='latin-1')
            print("\nOUTPUT:\n")
            print(result)
    
        file.close()



def main():

    serverSocket = connection()
    setup(serverSocket)

    while True:

        printOptions()
        scelta = input()
        
        if scelta == "1":
            shell(serverSocket)

        elif scelta == "2":
            serverSocket.send("esc".encode(encoding='latin-1'))
            break
        
        else:
            print("Inserisci un numero valido")

    serverSocket.close()
    print("Connection closed\n")



if __name__== "__main__" :
    main()

