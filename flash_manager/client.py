# client.py  
import socket
import sys
import time

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                     

if(len(sys.argv) < 2):
  print"Please input the command.\n"
  sys.exit(1)

msg = sys.argv[1]

host = "127.0.0.1"

if(msg == "flash"):
  port = 8888
  print "Send %s request to flash board control manager.\n" %msg
  answer_time = 60
elif(msg == "reboot"):
  port = 8889
  print "Send %s request to ETH board control manager.\n" %msg
  answer_time = 10
else:
  print "command not supported.\n"
  sys.exit(1)

# connection to hostname on the port.
s.connect((host, port))                         

s.send(msg)

# Receive no more than 1024 bytes
msg=s.recv(1024)

s.close()

print("Receive answer from Manager: ", msg)


