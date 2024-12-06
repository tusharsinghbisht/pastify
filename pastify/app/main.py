import socket
from .defaults import *
from .handler import Request, Response
from .error import *
from pastify.utils.message import message
from functools import wraps
from .RESPONSES import *
from .router import Router

class Pastify:
    '''
    A simple web server implementation to handle HTTP requests and serve responses.
    '''
    def __init__(self, HOST=DEFAULT_SERVER_HOST, PORT=DEFAULT_SERVER_PORT):
        """
        Initializes the server by creating a socket, binding to the provided host and port.

        ### Parameters:
            HOST (str): The host address (default: DEFAULT_SERVER_HOST).
            PORT (int): The port number (default: DEFAULT_SERVER_PORT).
        
        ### Raises:
            SocketFailure: If socket creation fails.
        """
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
        self.middlewares = []

    def use(self, middleware):
        '''
        Registers a middleware function to be applied to all incoming requests.

        ### Parameters:
            middleware (callable): A function that accepts Request and Response objects.
        '''
        self.middlewares.append(middleware)


    def route(self, path:str,  allowed_methods:list, middlewares:list=[]):
        '''
        Used to define a route

        ### Parameter
            - `path (str)`: path for route
            - `allowed_methods (list)`: array/list of allowed methods (GET, POST etc)
            - `middlewares (list)`: list of middlewares for a particular route
        '''
        def decorator(handler):
            self.route_map[path] = [handler, allowed_methods, any([v[0] == ":" for v in path.split("/") if v ]), middlewares]
            @wraps(handler)
            def wrapper(req: Request, res: Response):
                return handler(req, res)
            return wrapper
        return decorator
    
    def search_route_param(self, url: str):
        '''
        Searches for dynamic parameters in the route and returns the corresponding handler.

        ### Parameters:
            url (str): The requested URL.

        ### Returns:
            tuple: A tuple containing the matched route and a dictionary of route parameters.

        ### Raises:
            RouteNotFound: If no matching route is found.
        '''
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
        '''
        Handles incoming request

        ### Parameter
            - `req (Request)`: request object created from data of incoming request

        ### Raises:
            - `InternalServerError`: If there is an issue handling the request.
            - `MethodNotAllowed`: If the HTTP method is not allowed for the route.
            - `RouteNotFound`: If the route does not exist.
            - `FileNotExist`: If the requested file does not exist.
            - `TemplateError`: If there is an error rendering a template.
        '''
        try:
            res = Response(req)

            route, params = self.search_route_param(req.base_url)
            handler, allowed_methods, is_param, route_middlewares = self.route_map[route]
            req.params = params

            if req.method not in allowed_methods:
                raise MethodNotAllowed(allowed_methods)
            
            for middleware in self.middlewares + route_middlewares:
                if callable(middleware):
                    if not res.sent:
                        middleware(req, res)
                else:
                    print("Invalid middleware as argument")
                    raise InternalServerError


            # handler(req, res)
            if not res.sent:
                handler(req, res)

            if not res.sent:
                raise InternalServerError
            message.blue(f"Response Sent: {res.getStatus()}")

        except InternalServerError:
            res.status(500)
            res.message("Internal server error")
            res.send(INTERNAL_SERVER_ERROR_PAGE)
            message.red(f"RESPONSE sent: {res.getStatus()}")

        except MethodNotAllowed:
            res.status(405)
            res.message("Method not allowed")
            res.send(METHOD_NOT_ALLOWED_PAGE)
            message.red(f"RESPONSE sent: {res.getStatus()}")

        except (RouteNotFound,FileNotExist):
            res.status(404)
            res.message("Resource not found")
            res.send(NOT_FOUND_PAGE)
            message.red(f"RESPONSE sent: {res.getStatus()}")
        except TemplateError as e:
            res.status(e.status_code)
            res.message(e)
            res.send(TEMPLATE_ERROR_PAGE(e))
            message.red(f'RESPONSE sent: {res.getStatus()}')

            # create a Request, Response class to check inter package imports


    def mainloop(self):
        '''For the continuous listening loop of the server'''
        try:
            client_socket, client_address = self.server_socket.accept()
            req = Request(client_socket)
            
            print(f"\nIncoming REQUEST: {req.url} [{req.method}]")
            
            self.handleRequest(req)

        except KeyboardInterrupt:
            message.red("\nServer Stopped by user...")
            exit()
        except (OSError, SeverOverflowError):
            pass


    def listen(self, callback:callable=None):
        '''
        Starts the server and begins listening for incoming requests.

        ### Parameters:
            callback (callable, optional): A function to be called once the server starts listening.
        
        #### If callback is provided, it will be called with "OK" and a success message.
        '''
        self.server_socket.listen(5)
        
        if callback != None:
            callback("OK", f"Server listening on port {self.port}")
        
        while self.is_running:
            self.mainloop()
            

    def useStatic(self, directory:str, route:str="/static"):
        '''
        Serves static files from the specified directory.

        ### Parameters:
            directory (str): The directory where static files are stored.
            route (str): The URL route for serving static files (default: "/static").
        '''
        if route == "/":
            route = ""

        @self.route(path=f"{route}/:file", allowed_methods=["GET"])
        def static(req, res):
            file = req.params["file"]
            res.fsend(f"{directory}/"+file)

    def useRouter(self, router: Router):
        '''
        Integrates another Router instance into the current server's route map. Also used to club route with particular prefix together.

        ### Parameters:
            - `router (Router)`: The Router instance whose routes should be included.
        '''
        self.route_map.update(router.route_map)

    def shutdown(self):
        '''
        Stops the server by shutting down the socket connection and closing it.

        ### This method is called to stop the server gracefully.
        '''
        self.is_running = False
        try:
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
        except OSError:
            pass