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
            self.route_map[path] = [handler, allowed_methods, any([v[0] == ":" for v in path.split("/") if v ])]
            @wraps(handler)
            def wrapper(*args, **kwargs):
                return handler(*args, **kwargs)
            return wrapper
        return decorator
    
    def search_route_param(self, url):
        url = url[0] + url.strip("/")  # remove extra / from left and right
        # if url in route_map and route doesn't have any params
        if url in self.route_map.keys() and not self.route_map[url][2]:
            return (url, {})

        url_tokens = [v for v in url.split("/") if v]

        for route in self.route_map.keys():
            curr_url_tokens = [v for v in route.split("/") if v]
            # print(curr_url_tokens, url_tokens)

            if not self.route_map[route][2]:
                if curr_url_tokens == url_tokens:
                    return (route, {})
            else:
                ret = True
                if len(url_tokens) == len(curr_url_tokens):
                    params = {}
                    for x, y in zip(url_tokens, curr_url_tokens):
                        if y[0] == ":":
                            params[y[1:]] = x
                        elif x != y:
                            ret = False
                    if ret:
                        return (route, params)

        raise RouteNotFound(url)
    
    

    def handleRequest(self, req: Request):
        try:
            res = Response(req)

            route, params = self.search_route_param(req.base_url)
            handler, allowed_methods, is_param = self.route_map[route]
            req.params = params

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

        except RouteNotFound as e:
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

        except KeyboardInterrupt:
            print("Server Stopped by user..")
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