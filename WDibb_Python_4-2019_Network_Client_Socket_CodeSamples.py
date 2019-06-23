#!/usr/bin/env python
# coding: utf-8

# In[1]:


#### 4-2019 Will Dibb coursework code samples
#### Code prompts written by Cris Doloc
#### Code independently written by Will Dibb
#### TCP/UDP Socket Network Clients

#Code a TCP Client and a TCP Server 
#that exchange information such that the Client sends a request to Server in the form of a 
#string (put a time-stamp on it), and the Server responds back (put a time-stamp on it as well)
#to it to the Client that prints it at the console)time-stamped again).

#Implement the same requirements for the UDP protocol.


# In[1]:


#TCP Client
import socket
import time

# create a socket object, SOCK_STREAM is TC protocol 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9995
#Submit 

# connection to hostname on the port.
s.connect((host, port))                               
client_query = 'What is the best color?'
time_stamp = time.ctime(time.time()) + '\r\n'
print('Client query issued:', client_query, 'at', time_stamp)
s.send(client_query.encode())
# Receive no more than 2048 bytes
time_stamp = s.recv(2048)  
color = s.recv(2048)



print('\nServer color query response is:', color.decode(), 'at', time_stamp.decode('ascii'))


# In[2]:


#UDP Client
import socket
import sys
import time

# Create a SOCK_DGRAM UD protocol socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 9991)
client_query = 'What is the best shape?'
time_stamp = time.ctime(time.time()) + '\r\n'

try:

    #Sending client side query
    print('Client query issued:', client_query, 'at', time_stamp)
    sent = clientsocket.sendto(client_query.encode(), server_address)
    # Receive response
    print('Waiting to receive server response...')
    shape_resp, server = clientsocket.recvfrom(4096)
    response = shape_resp.decode()
    print('Received server response: ', response, 'at', time_stamp)

finally:
    print('Socket closed.')
    clientsocket.close()


# In[ ]:




