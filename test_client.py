# Echo server program
import socket
import threading

def listener():
    while 1:
        print(s.recv(1024).decode("ascii"))
def sender():
    while 1:
        msg = input().encode("ascii")
        s.send()

host = '127.0.0.1'                 # Symbolic name meaning the local host
port = 8181                        # Arbitrary non-privileged port

# create an INET, STREAMing socket - don't worry too much about this
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to " + host + ":" + str(port))
s.connect((host, port))

# accept header
msg = s.recv(1024)
print(msg.decode('ascii'))

threads = []
threads[0] = threading.Thread(target=listener())
threads[1] = threading.Thread(target=sender())
for thread in threads:
    thread.start()


# close connection
s.close()
