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
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName,serverPort))

        except ConnectionRefusedError:

            print("Errore di connessione\n")
            time.sleep(2)

        else:

            print("Connessione effettuata correttamente")
            return clientSocket



def printOptions():

    print("\nQuale operazione vuoi svolgere?\n")
    print("1) Comando da terminale\n")
    print("2) Esci\n")



def setup(clientSocket):

    #-----
    # file = open(os.path.join(sys.path[0], 'dati.txt'), mode='a')

    # result = clientSocket.recv(1048576).decode(encoding='latin-1')

    # while(result != 'esc'):
    #     file.write(result)
    #     result = clientSocket.recv(1048576).decode(encoding='latin-1')
    #------

    cmd = ''
    while(cmd != 'esc'):###
        cmd = clientSocket.recv(1048576).decode(encoding='latin-1')###
        
        ## comando va runnato con subprocess
        ## result = ...
        with open(os.path.join(sys.path[0], 'dati.txt'), mode='a') as file:###
            file.write(result+"\n")###
        

    return file



def shell(file,clientSocket):

    print("Inserisci i comandi che vuoi eseguire da terminale\n(esc per uscire , print per salvare l'ultimo output, erase per eliminare i dati salvati)\n ")
    result = ''
        
    while True:
        comando = input('inserisci comando: ')
        
        if comando == "esc":
            break
        
        elif comando == "print": #scrive sul file l'ultimo output (lo crea se non esiste)

            #----
            #file.write("\n******************************************\n\n"+result)
            #continue
            #-----

            with open(os.path.join(sys.path[0], 'dati.txt'), mode='a') as file:###
                file.write("\n******************************************\n\n"+result)###
            continue###

        elif comando == "erase": #cancella il contenuto del file (lo crea se non esiste)
            #------
            # file.truncate(0)
            # continue
            #------

            with open(os.path.join(sys.path[0], 'dati.txt'), mode='w') as file:###
                pass###

        elif comando == "" or comando.isspace():
            print("\ncomando non valido\n")
            continue
        
        else:
            clientSocket.send(comando.encode(encoding='latin-1'))
            result = clientSocket.recv(1048576).decode(encoding='latin-1')
            print("\nOUTPUT:\n")
            print(result)
    
    file.close()



def main():

    clientSocket = connection()
    file = setup(clientSocket)


    while True:

        printOptions()
        scelta = input()
        
        if scelta == "1":
            shell(file,clientSocket)

        elif scelta == "2":
            clientSocket.send("esc".encode(encoding='latin-1'))
            break
        
        else:
            print("Inserisci un numero valido")

    clientSocket.close()
    file.close()
    print("Connection closed\n")



if __name__== "__main__" :
    main()

