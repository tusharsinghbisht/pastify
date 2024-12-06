
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

class FileNotExist(Exception):
    def __init__(self):
        super().__init__(f"The file you are trying to access is unavailable")

class InternalServerError(Exception):
    def __init__(self, message="Internal server error occurred"):
        super().__init__(message)


class TemplateError(Exception):
    def __init__(self, message="Invalid template", status_code=404):
        super().__init__(message)
        self.status_code = status_code

class SeverOverflowError(Exception):
    def __init__(self):
        super().__init__("Sever not optimized for this much of data")