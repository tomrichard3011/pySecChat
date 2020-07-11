import socket
import threading
import queue
import time


class NetworkManager:
    def __init__(self, host: str, port: int, input_q: queue.SimpleQueue, output_q: queue.SimpleQueue):
        self.host = host
        self.port = port
        self.input_q = input_q
        self.output_q = output_q

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        in_thread = threading.Thread(target=self.input_thread)
        out_thread = threading.Thread(target=self.output_thread)
        in_thread.daemon = True
        out_thread.daemon = True

        in_thread.start()
        out_thread.start()

    def input_thread(self):
        while 1:
            if not self.input_q.empty():
                msg = self.input_q.get()
                self.output_q.put(msg)
                self.server.send(msg.encode('ascii'))
            time.sleep(.2)

    def output_thread(self):
        while 1:
            msg = self.server.recv(1024).decode('ascii')
            self.output_q.put(msg)
