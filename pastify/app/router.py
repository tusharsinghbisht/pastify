from functools import wraps
from .handler import Request, Response

class Router:
    """
    Router class for managing routes, handlers, and middleware for a particular parent route.

    Attributes:
        route_map (dict): A dictionary of routes mapped to handlers, methods, and middleware.
        parent_route (str): The base route to be prefixed to all defined routes.
        middlewares (list): Global middlewares for all routes in this router.
    """

    def __init__(self, parent_route:str="", middlewares:list=[]):
        """
        Initializes the Router instance.

        Parameters:
            parent_route (str): The base route to be prefixed (default: "").
            middlewares (list): Global middlewares (default: []).
        """
        self.route_map = {}
        self.parent_route = parent_route
        self.middlewares = middlewares

    def route(self, path: str, allowed_methods: list, middlewares: list = []):
        """
        Defines a route and associates it with a handler.

        Parameters:
            - `path (str)`: The route path, it is prefixed with Router's `parent_route`.
            - `allowed_methods (list)`: HTTP methods for the route.
            - `middlewares (list)`: Middlewares specific to the route (default: []).
        
        """
        def decorator(handler):
            full_path = self.parent_route + path
            self.route_map[full_path] = [
                handler,
                allowed_methods,
                any([v[0] == ":" for v in full_path.split("/") if v]),
                self.middlewares + middlewares
            ]

            @wraps(handler)
            def wrapper(req: Request, res: Response):
                return handler(req, res)

            return wrapper

        return decorator
