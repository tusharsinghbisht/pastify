
class SocketFailure(Exception):
    def __init__(self):
        super().__init__("Socket failure")

class MethodNotAllowed(Exception):
    def __init__(self, allowed_methods):
        message = f"Current method is not allowed for this resource, allowed methods: {allowed_methods}"
        super().__init__(message)

        