from socket import *
import os
import sys

serverName = '192.168.1.172' #e' un nome simbolico, che il DNS (un sistema interno) che lo traduce in IP
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

def printOptions():
    print("\nQuale operazione vuoi svolgere?\n")
    print("1) Comando da terminale\n")
    print("2) Esci\n")
    

while True:
    
    printOptions()
    scelta = input("Inserisci opzione: ")
    print("\n")
    result = ''
    comando = ''
    
    if scelta == "1":
        result = ''
        print("Inserisci i comandi che vuoi eseguire da terminale\n(esc per uscire , print per salvare l'ultimo output, erase per eliminare i dati salvati)\n ")
        
        while True:
            comando = input('inserisci comando: ')
            
            if comando == "esc":
                break
            
            elif comando == "print": #scrive sul file l'ultimo output (lo crea se non esiste)
                try:
                    filePath = os.path.join(sys.path[0], 'dati.txt')
                    with open(filePath, mode='a') as file:
                        file.write("\n******************************************\n\n"+result)
                    continue
                except error as e:
                    print(e)
                
            elif comando == "erase": #cancella il contenuto del file (lo crea se non esiste)
                filePath = os.path.join(sys.path[0], 'dati.txt')
                with open(filePath, mode='w') as file:
                    pass
                continue
            
            elif comando == "" or comando.isspace():
                comando = "comando non valido"
                
            clientSocket.send(comando.encode(encoding='latin-1'))
            result = clientSocket.recv(1048576).decode(encoding='latin-1')
            print("\nOUTPUT:")
            print(result)
            
    elif scelta == "2":
        break
    
    else:
        print("Inserisci un numero valido")










