# Echo server program
import socket

host = '127.0.0.1'                 # Symbolic name meaning the local host
port = 8181              # Arbitrary non-privileged port
# create an INET, STREAMing socket - don't worry too much about this
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Created open port on: " + str(port))

#bind our program to a specific port on a specific host
s.bind((host, port))

# accept 1 connection
s.listen(1)

# s.accept returns connection object, and IP address and port of connection
conn, addr = s.accept()
print('Connected by', addr)

# can only send byte(ascii) code over network, no strings, ints, etc.
conn.send("Welcome to the example!\n".encode('ascii'))

while 1:
    conn.send("Enter your name: ".encode('ascii'))

    # recieve message
    data = conn.recv(1024)
    if not data: break
    # print message recieved, must decode byte to string
    print("Recieved: " + data.decode('ascii'))

    # craft message to send back, must encode string to byte
    msg = 'Hello ' + data.decode('ascii')
    print("Sending: " + msg)
    msg = msg.encode('ascii')
    # send message back
    conn.send(msg)
conn.close()

