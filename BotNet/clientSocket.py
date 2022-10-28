import subprocess
from socket import *
import os

serverName = 'localhost' #e' un nome simbolico, che il DNS (un sistema interno) che lo traduce in IP
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

while True:
    comando = input('inserisci comando: ')
    clientSocket.send(comando.encode())
    result = clientSocket.recv(16536).decode()
    print(result)




# cat /etc/machine-id -------- id macchina
# cat /etc/os-release --------- info generali os
# cat /proc/meminfo ------ info memoria
# cat /proc/cpuinfo ----- info dettagliate di ogni core
# lscpu ---- info architettura cpu
# lspci ------- info schede (video, audio...)
# lsusb ------ info dispositivi usb