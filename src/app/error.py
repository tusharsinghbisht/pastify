
class SocketFailure(Exception):
    def __init__(self):
        super().__init__("Socket failure")

class MethodNotAllowed(Exception):
    def __init__(self, allowed_methods):
        message = f"Current method is not allowed for this resource, allowed methods: {allowed_methods}"
        super().__init__(message)

class RouteNotFound(Exception):
    def __init__(self, route):
        super().__init__(f"The resource {route} you are trying to access is unavailable")