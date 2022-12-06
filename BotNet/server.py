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
    print("1) Connessione ad un client\n")
    print("2) Esci\n")



def setup(serverSocket):

    file = open(os.path.join(sys.path[0], 'dati.txt'), mode='a')
    
    result = (str)(serverSocket.recv(1048576).decode())

    while not(result.endswith("uscita")):
        file.write("\n******************************************\n\n"+result)
        result = (str)(serverSocket.recv(1048576).decode())
    
    file.write("\n******************************************\n\n"+result.rstrip('uscita'))
            
    file.close()
    

    
def download(fileName, connectionSocket):

    try:
        file = open(fileName, "wb")
        data = connectionSocket.recv(1024)

        while not (str(data)).endswith("esc'"):
            file.write(data)
            data = connectionSocket.recv(1024)

        file.close()

    except:
        print("Errore durante il download del file\n")
        file.close()


def shell(serverSocket):
    

    print("Inserisci i comandi che vuoi eseguire da terminale\n(esc per uscire , print per salvare l'ultimo output, erase per eliminare i dati salvati)\n ")
    result = ''
        
            
    while True:

        file = open(os.path.join(sys.path[0], 'dati.txt'), mode='a' )


        try:

            comando = input('inserisci comando: ')
            
            if comando == "esc":
                file.close()
                break

            try:

                if comando == "recv":
                    result = serverSocket.recv(1048576).decode()
                    print(result)
                    continue            

            except KeyboardInterrupt:
                print("\n")
                continue


            if comando.startswith("download"):
                serverSocket.send(comando.encode())
                download(comando[9:], serverSocket)
                continue

            
            if comando == "print": #scrive sul file l'ultimo output (lo crea se non esiste)
                file.write("\n******************************************\n\n"+result)
                continue

            if comando == "erase": #cancella il contenuto del file (lo crea se non esiste)
                file.truncate(0)
                continue

            if comando == "" or comando.isspace():
                print("\ncomando non valido\n")
                continue
            
            else:
                serverSocket.send(comando.encode())
                result = serverSocket.recv(1048576).decode()
                print("\nOUTPUT:\n")
                print(result)
        
            file.close()

        except KeyboardInterrupt:
            continue




def main():


    while True:

        printOptions()
        scelta = input()
        
        if scelta == "1":
            serverSocket = connection()
            
            setup(serverSocket)
            shell(serverSocket)
            
            serverSocket.send("esc".encode())
            serverSocket.close()

        elif scelta == "2":
            break
        
        else:
            print("Inserisci un numero valido")


    print("Connection closed\n")



if __name__== "__main__" :
    main()

