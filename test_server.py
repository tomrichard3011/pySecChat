# Echo server program
import socket
import threading

def listener():
    while 1:
        print(conn.recv(1024).decode("ascii"))
def sender():
    while 1:
        msg = input().encode("ascii")
        conn.send(msg)

host = '127.0.0.1'                 # Symbolic name meaning the local host
port = 8181              # Arbitrary non-privileged port
# create an INET, STREAMing socket - don't worry too much about this
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind our program to a specific port on a specific host
s.bind((host, port))
print("Created open port on: " + str(port))

# accept 1 connection
s.listen(1)

# s.accept returns connection object, and IP address and port of connection
conn, addr = s.accept()
print('Connected by', addr)

# send header
conn.send("Welcome to the example!\nThis is a header, it can contain information on the type of program that we run on this port.\nI will echo back any text you send me.".encode('ascii'))

threads = []
threads[0] = threading.Thread(target=listener())
threads[1] = threading.Thread(target=sender())
for thread in threads:
    thread.start()

conn.close()
