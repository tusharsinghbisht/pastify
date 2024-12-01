import socket
from .defaults import *
from .handler import Request, Response
from .error import *
from utils.message import message
from functools import wraps
import threading

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
    
    def search_route_param(self, url):
        if url in self.route_map.keys():
            return (url, {})

        og_url = url.split("/")

        for route in self.route_map.keys():
            this_url = route.split("/")
            print(route,this_url)
            if len(og_url) == len(this_url) and og_url[0:-1] == this_url[0:-1] and this_url[-1][0] == ":":
                print(og_url)
                return (route, { this_url[-1][1:]: og_url[-1] })

        raise KeyError
    
    

    def handleRequest(self, req: Request):
        try:
            res = Response(req)

            route, params = self.search_route_param(req.base_url)
            req.params = params
            handler, allowed_methods = self.route_map[route]

            if req.method not in allowed_methods:
                raise MethodNotAllowed(allowed_methods)

            # handler(req, res)
            handler(req, res)

            message.blue("Response Sent")

        except MethodNotAllowed:
            res.status(405)
            res.message("Method not allowed")
            res.send("<h1>Method Not Allowed</h1><p>The method you are using to access the resource is not allowed</p>")
            message.red("RESPONSE sent: Method not allowed")

        except KeyError:
            res.status(404)
            res.message("Resource not found")
            res.send("<h1>Resource not found</h1><p>The resource you are trying to access is not available</p>")
            message.red("RESPONSE sent: Resource not found")

            # create a Request, Response class to check inter package imports


    def mainloop(self):
        try:
            client_socket, client_address = self.server_socket.accept()
            req = Request(client_socket)
            # print(req)
            
            print(f"\nIncoming REQUEST: {req.url} [{req.method}]")
            
            self.handleRequest(req)
        except OSError:
            pass

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
            # loop = threading.Thread(target=self.mainloop())
            # loop.start()
            
        # print("shut down triggerd")

    def shutdown(self):
        self.is_running = False
        try:
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
        except OSError:
            pass