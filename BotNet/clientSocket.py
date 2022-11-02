import subprocess
from socket import *
import os

serverName = 'localhost' #e' un nome simbolico, che il DNS (un sistema interno) che lo traduce in IP
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

def printOptions():
    print("\nQuale operazione vuoi svolgere?\n")
    print("1) Comando da terminale\n")
    print("2) Recupera informazioni macchina\n")
    print("3) Esci\n")

while True:
    printOptions()
    scelta = input("Inserisci opzione: ")
    print("\n")
    if scelta == "1":
        print("Inserisci i comandi che vuoi eseguire da terminale oppure esc per uscire: ")
        comando = ""
        while True:
            comando = input('inserisci comando: ')
            if(comando == "esc"):
                break
            clientSocket.send(comando.encode(encoding='cp1252'))
            result = clientSocket.recv(16536).decode(encoding='cp1252')
            print("\nOUTPUT:")
            print(result)
    elif scelta == "2":
        #recupero informazioni varie
        print("info")
    elif scelta == "3":
        break
    else:
        print("Inserisci un numero valido")










