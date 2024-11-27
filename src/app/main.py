import socket
from .defaults import *


class Pastify:
    '''
    Creating a basic pastify server
    Specify HOST (hostname), PORT (port number)
    '''
    def __init__(self, HOST=DEFAULT_SERVER_HOST, PORT=DEFAULT_SERVER_PORT):
         # initialzing socket
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created...")
        except:
            raise Exception("Error creating socket...")
        
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Setting connection to TCP 
        self.server_socket.bind((HOST, PORT)) # binding socket to given HOST and PORT

        self.hostname = HOST
        self.port = PORT
        self.route_map = []


    def route(self, path, handler, methods):
        self.route_map.append({ path: [handler, methods] })

    def handleRequest(self, request):
        try:
            handler, methods = self.route_map["path"]
        except KeyError:
            # res = "HTTP/1.1 405 Method Not Allowed\n\n<h1>Invalid Method</h1>"
            # client_socket.sendall(res.encode())

            # create a Request, Response class to check inter package imports


    def listen(self, callback):
        self.server_socket.listen(5)

        callback({ "status": "OK", "message": f"Server listening on port {self.port}" })

        while True:
            client_socket, client_address = self.server_socket.accept()

            req = client_socket.recv(1500).decode()
            headers = req.split("\n")
            
            method, path, http_version = headers[0].split()
            
            if method == "GET":
                if path == "/":
                    fin = open("index.html", "r")
                    content = fin.read()
                    fin.close()

                    # sending response
                    # STATUS LINE
                    # HEADERS
                    # MESSAGE-BODY
                    res = "HTTP/1.1 200 OK\n\n" + content
                    client_socket.sendall(res.encode())
                    client_socket.close()
            else:
                res = "HTTP/1.1 405 Method Not Allowed\n\n<h1>Invalid Method</h1>"
                client_socket.sendall(res.encode())