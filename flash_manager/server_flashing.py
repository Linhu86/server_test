# server.py 
import socket                                         
import time
from subprocess import check_output

print "Start flash board control Manager.\n";

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# define host ip and port 
host = "127.0.0.1"
port = 8888

def flash_do():
    print "Start to flash board.\n";
    check_output("cd \"C:\userdata\programs\EasyFlash\" && shell_EasyFlash.exe", shell=True)
 

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)                                      

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()

    msg = clientsocket.recv(1024)

    print("Got a connection from %s with command: %s" %(str(addr), msg))
	
    flash_do()
      
    clientsocket.send("Flash board OK.\n")
    print "Flash board OK\n"

clientsocket.close()
serversocket.close()