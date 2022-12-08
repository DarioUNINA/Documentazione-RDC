from socket import *
import os
import sys



def connection():

    serverPort = 11926
    serverSocket = socket(AF_INET,SOCK_STREAM)

    serverSocket.bind( ('',serverPort) )
    serverSocket.listen(1)

    print ("The Server is ready to receive")

    serverSocket, addr = serverSocket.accept()
    print("Accepted a new client", addr)

    return serverSocket


def printOptions():

    print("\nQuale operazione vuoi svolgere?\n")
    print("1) Connessione ad un client\n")
    print("2) Esci\n")


def setup(serverSocket):

    file = open(os.path.join(sys.path[0], 'dati.txt'), mode='a')
    
    result = (str)(serverSocket.recv(1048576).decode(encoding="latin-1"))

    while not(result.endswith("uscita")):
        file.write("\n******************************************\n\n"+result)
        result = (str)(serverSocket.recv(1048576).decode(encoding="latin-1"))
    
    file.write("\n******************************************\n\n"+result.rstrip('uscita'))
            
    file.close()
    
    
def download(fileName, connectionSocket):

    try:
        file = open(fileName, "wb")
        data = connectionSocket.recv(1024)

        while not (str(data)).endswith("esc'"):
            file.write(data)
            data = connectionSocket.recv(1024)

        file.write(data)
        file.close()

    except Exception as e:
        print("Error during file download\n")
        file.close()


def shell(serverSocket):
    

    print("Inserisci i comandi che vuoi eseguire da terminale\n(esc per uscire , print per salvare l'ultimo output, erase per eliminare i dati salvati, download [nomeFile.estensione] per salvare una copia locale di nomeFile.estensione)\n ")
    result = ''
        
    while True:

        file = open(os.path.join(sys.path[0], 'dati.txt'), mode='a' )

        try:

            comando = input('inserisci comando: ')
            
            if comando == "esc":
                file.close()
                break

            if comando.startswith("download"):
                serverSocket.send(comando.encode(encoding="latin-1"))
                download(comando[9:], serverSocket)
                continue

            
            if comando == "print":
                file.write("\n******************************************\n\n"+result)
                continue

            if comando == "erase":
                file.truncate(0)
                continue

            if comando == "" or comando.isspace():
                print("\nInvalid commands\n")
                continue

            
            try:

                if comando == "recv":
                    result = serverSocket.recv(1048576).decode(encoding="latin-1")
                    print(result)
                    continue            

            except KeyboardInterrupt:
                print("\n")
                continue


            else:
                serverSocket.send(comando.encode(encoding="latin-1"))
                result = serverSocket.recv(1048576).decode(encoding="latin-1")

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
            
            serverSocket.send("esc".encode(encoding="latin-1"))
            serverSocket.close()

        elif scelta == "2":
            break
        
        else:
            print("Choose any valid number\n")


    print("Connection closed\n")


if __name__== "__main__" :
    main()

