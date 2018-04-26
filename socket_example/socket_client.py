# Import socket module
import socket               
import sys
 
# Create a socket object
s = socket.socket()         
 
# Define the port on which you want to connect
port = 12345               
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))
 
 
s.send(sys.argv[1])


# close the connection
s.close()  
