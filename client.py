import curses
import client_ui
import client_socket
import queue
host = '127.0.0.1'
port = 8181

# chat queue for shared memory
input_q = queue.SimpleQueue()

# if you want to output something to the screen, add it to output_q
output_q = queue.SimpleQueue()

# try connecting to the server
net_man = client_socket.NetworkManager(host, port, input_q, output_q)

# initiate UI window
curses.wrapper(client_ui.ui(input_q, output_q).run)
