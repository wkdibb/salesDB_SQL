#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#### 4-2019 code prompts written by Cris Doloc
#### Code independently written by Will Dibb
#### TCP/UDP Socket Servers

#TCP Server

#Code a TCP Client and a TCP Server 
#that exchange information such that the Client sends a request to Server in the form of a 
#string (put a time-stamp on it), and the Server responds back (put a time-stamp on it as well)
#to it to the Client that prints it at the console)time-stamped again).

#Implement the same requirements for the UDP protocol.


# In[ ]:


#TCP Server
import socket                                         
import time

# create a socket object, SOCK_STREAM is TC protocol 
serversocket = socket.socket(socket.AF_INET, 
                             socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

#set arbitrary non-secured port
port = 9995                                           

# bind to the port
serversocket.bind((host, port))   
print('Socket bound.')

# queue up to 3 requests
serversocket.listen(3) 
print('Waiting for connections...')

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()      
    time_stamp = time.ctime(time.time()) + '\r\n'
    print('Received connection from ', str(addr), 'at ', time_stamp)
    client_query = clientsocket.recv(2048)
    print('Connection query:', client_query.decode())
    color = ('purple')
    
    clientsocket.send(time_stamp.encode('ascii'))
    clientsocket.send(color.encode())
    print('\nThe objectively superior color', color, 
          'submitted in response to client color query, at', time_stamp)
    print('Socket closed.')
    clientsocket.close()


# In[ ]:


#UDP Server

import socket
import sys
import time

# Create a SOCK_DGRAM UD protocol socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind socket to the port
server_address = ('127.0.0.1', 9991)
print('Starting UDP connection...')
serversocket.bind(server_address)

while True:
    client_query, addr = serversocket.recvfrom(4096)
    time_stamp = time.ctime(time.time()) + '\r\n'
    print('Received connection from ', str(addr), 'at ', time_stamp)
    print('Received client query: ', client_query.decode())
    shape = ('rhombus')
    
    serversocket.sendto(shape.encode(), addr)
    print('Sent shape [', shape, '] as response to client query at', time_stamp)
    print('Waiting for next connection...')


# In[ ]:




