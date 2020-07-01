# Echo server program
import socket

host = '127.0.0.1'                 # Symbolic name meaning the local host
port = 8181                        # Arbitrary non-privileged port

# create an INET, STREAMing socket - don't worry too much about this
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# send header
print("Connecting to " + host + ":" + str(port))

s.connect((host, port))

# accept header
msg = s.recv(1024)
print(msg.decode('ascii'))

# send message
s.send("generic name".encode('ascii'))

# recieve response
msg = s.recv(1024)
print(msg.decode('ascii'))

# close connection
s.close()
