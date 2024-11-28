import socket
from .defaults import *
from .handler import Request, Response
from .error import *
from utils.message import message
from functools import wraps

class Pastify:
    '''
    Creating a basic pastify server
    Specify HOST (hostname), PORT (port number)
    '''
    def __init__(self, HOST=DEFAULT_SERVER_HOST, PORT=DEFAULT_SERVER_PORT):
         # initialzing socket
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            message.pink("Socket created...")
        except:
            raise SocketFailure()
        
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Setting connection to TCP 
        self.server_socket.bind((HOST, PORT)) # binding socket to given HOST and PORT

        self.hostname = HOST
        self.port = PORT
        self.route_map = {}


    def route(self, path,  allowed_methods):
        def decorator(handler):
            self.route_map[path] = [handler, allowed_methods]
            @wraps(handler)
            def wrapper(*args, **kwargs):
                return handler(*args, **kwargs)
            return wrapper
        return decorator

    def handleRequest(self, path, client_socket, method):
        try:
            handler, allowed_methods = self.route_map[path]

            if method not in allowed_methods:
                raise MethodNotAllowed(allowed_methods)

            handler(client_socket)

            message.blue("Response Sent")

        except MethodNotAllowed:
            res = "HTTP/1.1 405 Method Not Allowed\n\n<h1>Method Not Allowed</h1><p>The method you are using to access the resource is not allowed</p>"
            message.red("RESPONSE sent: Method not allowed")
            client_socket.sendall(res.encode())
            client_socket.close()

        except KeyError:
            res = "HTTP/1.1 404 Resource not found\n\n<h1>Resource not found</h1><p>The resource you are trying to access is not available</p>"
            message.red("RESPONSE sent: Resource not found")
            client_socket.sendall(res.encode())
            client_socket.close()

            # create a Request, Response class to check inter package imports


    def mainloop(self):
        client_socket, client_address = self.server_socket.accept()
        req = client_socket.recv(1500).decode()
        headers = req.split("\n")
        import socket
from .defaults import *
from .handler import Request, Response
from .error import *
from utils.message import message
from functools import wraps

class Pastify:
    '''
    Creating a basic pastify server
    Specify HOST (hostname), PORT (port number)
    '''
    def __init__(self, HOST=DEFAULT_SERVER_HOST, PORT=DEFAULT_SERVER_PORT):
         # initialzing socket
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            message.pink("Socket created...")
        except:
            raise SocketFailure()
        
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Setting connection to TCP 
        self.server_socket.bind((HOST, PORT)) # binding socket to given HOST and PORT

        self.hostname = HOST
        self.port = PORT
        self.route_map = {}
        self.is_running = True


    def route(self, path,  allowed_methods):
        def decorator(handler):
            self.route_map[path] = [handler, allowed_methods]
            @wraps(handler)
            def wrapper(*args, **kwargs):
                return handler(*args, **kwargs)
            return wrapper
        return decorator

    def handleRequest(self, path, client_socket, method):
        try:
            handler, allowed_methods = self.route_map[path]

            if method not in allowed_methods:
                raise MethodNotAllowed(allowed_methods)

            handler(client_socket)

            message.blue("Response Sent")

        except MethodNotAllowed:
            res = "HTTP/1.1 405 Method Not Allowed\n\n<h1>Method Not Allowed</h1><p>The method you are using to access the resource is not allowed</p>"
            message.red("RESPONSE sent: Method not allowed")
            client_socket.sendall(res.encode())
            client_socket.close()

        except KeyError:
            res = "HTTP/1.1 404 Resource not found\n\n<h1>Resource not found</h1><p>The resource you are trying to access is not available</p>"
            message.red("RESPONSE sent: Resource not found")
            client_socket.sendall(res.encode())
            client_socket.close()

            # create a Request, Response class to check inter package imports


    def mainloop(self):
        client_socket, client_address = self.server_socket.accept()
        req = client_socket.recv(1500).decode()
        headers = req.split("\n")
        
        method, path, http_version = headers[0].split()

        message.cyan(f"Incoming REQUEST: {path} [{method}]")
        
        self.handleRequest(path, client_socket, method)

        # if method == "GET":
        #     if path == "/":
        #         fin = open("index.html", "r")
        #         content = fin.read()
        #         fin.close()

        #         # sending response
        #         # STATUS LINE
        #         # HEADERS
        #         # MESSAGE-BODY
        #         res = "HTTP/1.1 200 OK\n\n" + content
        #         client_socket.sendall(res.encode())
        #         client_socket.close()
        # else:
        #     res = "HTTP/1.1 405 Method Not Allowed\n\n<h1>Invalid Method</h1>"
        #     client_socket.sendall(res.encode())

    def listen(self, callback):
        self.server_socket.listen(5)

        callback({ "status": "OK", "message": f"Server listening on port {self.port}" })
        
        while self.is_running:
            self.mainloop()
            print(self.is_running)

    def shutdown(self):
        self.is_running = False
        self.server_socket.close()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.hostname, self.port)
        client.connect(server_address)
        client.sendall("GET /temp HTTP/1.1")
        client.close()
        # shutdown watcher and server upon change in file , later instead of shutdown making it restart project
        