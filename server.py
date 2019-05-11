import socket
import threading


class Server:
    clients = {}

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        self.sock.listen(5)

    def accept_connections(self):
        while True:
            conn, addr = self.sock.accept()
            print("Connected => %s:%s" % addr)
            message = "The Church of Antonement requests your name on behalf of the Shrike.\n"
            conn.send(bytes(message, "utf-8"))
            conn_thread = threading.Thread(target=self.handle_connection,
                                           args=(conn, addr))
            conn_thread.daemon = True
            conn_thread.start()

    def handle_connection(self, conn, addr):
        name = conn.recv(1024).decode("utf-8")
        welcome = "Welcome %s, when you want to quit type \q and hit ctrl c. \n" % name
        conn.send(bytes(welcome, "utf-8"))
        new_person = "%s has joined the three of pain!" % name
        self.send_messages_to_clients(bytes(new_person, "utf-8"))
        self.clients[conn] = name
        while True:
            message = conn.recv(1024)
            if message == bytes("\q", "utf-8"):
                print("Disconnected => %s:%s" % addr)
                self.close_connection(conn, name)
                break
            self.send_messages_to_clients(message, name + ": ")

    def send_messages_to_clients(self, message, name=""):
        for sock in list(self.clients):
            sock.send(bytes(name, "utf-8") + message)

    def close_connection(self, conn, name):
        conn.close()
        del self.clients[conn]
        message = "%s has entered back to the Web." % name
        self.send_messages_to_clients(bytes(message, "utf-8"))


HOST = ''
PORT = 5000

if __name__ == "__main__":
    server = Server()
    print("Waiting for a connection...")
    ACCEPT_THREAD = threading.Thread(target=server.accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.sock.close()
