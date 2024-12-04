from functools import wraps

class Router:
    def __init__(self, parent_route="", middlewares=[]):
        self.route_map = {}
        self.parent_route = parent_route
        self.middlewares = middlewares

    def route(self, path, allowed_methods, middlewares=[]):
        def decorator(handler):
            full_path = self.parent_route+path
            self.route_map[full_path] = [handler, allowed_methods, any([v[0] == ":" for v in full_path.split("/") if v ]), self.middlewares + middlewares]
            @wraps(handler)
            def wrapper(*args, **kwargs):
                return handler(*args, **kwargs)
            return wrapper
        return decorator