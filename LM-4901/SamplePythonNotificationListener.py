import socket
import sys

# this listens to notification stream from MSE and displays results in console.

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_address = ('0.0.0.0', 8000)                                # change this to your ip address
sock.bind(server_address)
# print >>sys.stderr, 'using %s port %s' % sock.getsockname()     # use this print statement for python2.7
print (sys.stderr,'using %s port %s' % sock.getsockname())        # use this print statement for python3
sock.listen(1)

while True:
   print (sys.stderr, 'waiting for a connection')                 # use this print statement for python3
   # print >>sys.stderr, 'waiting for a connection'               # use this print statement for python2.7
   connection, client_address = sock.accept()
   try:
       #print >>sys.stderr, 'client connected:', client_address   # use this print statement for python2.7
       print (sys.stderr, 'client connected:', client_address)    # use this print statement for python3
       while True:
           data = connection.recv(1024)                           # change this value, based on your needs.
           print (sys.stderr, 'received "%s"' % data)             # use this print statement for python3
           #print >>sys.stderr, 'received "%s"' % data            # use this print statement for python2.7
           if data:
               connection.sendall(data)
           else:
               break
   finally:
       connection.close()
