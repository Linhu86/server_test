import select
import socket
import threading

from manager import Manager

class Server():
    def __init__(self):
        HOST, PORT = "", 9999
        # create an INET, STREAMing socket
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket
        self.srv.bind((HOST, PORT))
        # Start listening
        self.srv.listen(5)

        self.inputs = [self.srv]
        while True:
            try:
                inputready, outputready, exceptready = select.select(self.inputs, [], [])
            except select.error as e:
                break
            except socket.error as e:
                break

            if self.srv in inputready:
                # Begin handling a new client
                client, address = self.srv.accept()
                # Create a new manager for the client add add the client to the list of active clients
                manager = Manager()
                thread = threading.Thread(target=self.handle_client, args=(client, address, manager.handler))
                thread.start()

    def handle_client(self, cli, addr, handler):
        while True:
            request = cli.recv(1024).decode()
            response, keep_conn = handler(request)
            # Send back the response
            cli.sendall(("%s\n" % response).encode())
            # Check if we have to close the connection with the client
            if not keep_conn:
                cli.close()
                break

if __name__ == "__main__":
    server = Server()
    