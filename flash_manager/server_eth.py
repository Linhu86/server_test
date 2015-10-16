# server.py 
import socket                                         
import time
import sys
from subprocess import check_output

print "Start ETH board control Manager.\n";

#define host ip and port
host = "127.0.0.1"
port = 8889

def reboot_do():
    print "Turn off the Toby board.\n"
    check_output("C:\\userdata\\jenkins\\workspace\\M39G_MV_FW_CI_TEST\\tools\\flashing\\eth008_off.exe 10.0.4.185 17494", shell=True)
    time.sleep(1)
    print "Turn on the Toby board.\n"
    check_output("C:\\userdata\\jenkins\\workspace\\M39G_MV_FW_CI_TEST\\tools\\flashing\\eth008_on.exe 10.0.4.185 17494", shell=True)

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)                    

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)                                   

while True:

    # establish a connection
    clientsocket,addr = serversocket.accept()
    msg = clientsocket.recv(1024)

    print("Got a connection from %s with command: %s" %(str(addr), msg))

    print "Start to reboot the Toby board.\n"

    reboot_do()
      
    clientsocket.send("Reboot board OK.")
    print "OK.\n"

clientsocket.close()
serversocket.close()