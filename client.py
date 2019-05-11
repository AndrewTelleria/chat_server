import socket
import threading


class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        rec_thread = threading.Thread(target=self.receive)
        rec_thread.start()

    def receive(self):
        while True:
            try:
                message = self.sock.recv(1024).decode("utf-8")
                print(message)
            except OSError:
                break

    def send(self):
        while True:
            message = input("")
            self.sock.send(bytes(message, "utf-8"))
            if message == "\q":
                print("disconnected")
                self.sock.close()


HOST = input("Enter host: ")
PORT = input("Enter port: ")

if not PORT:
    PORT = 5000
else:
    PORT = int(PORT)

client = Client()
client.send()
