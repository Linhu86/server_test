import socket

class Server():
    def __init__(self, handler):
        HOST, PORT = "", 9999
        # create an INET, STREAMing socket
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket
        self.srv.bind((HOST, PORT))
        # Start listening
        self.srv.listen(1)
        while True:
            (cli, addr) = self.srv.accept()
            # wait for a connection
            while True:
                request = cli.recv(1024).decode()
                response, keep_conn = handler(request)
                # Send back the response
                cli.sendall(("%s\n" % response).encode())
                # Check if we have to close the connection with the client
                if not keep_conn:
                    cli.close()
                    break

