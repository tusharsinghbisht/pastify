"""
All the custom error classes used in error handling.

This module provides custom exceptions for handling specific errors
that may occur in the application, such as socket failures, route
issues, template errors, and server overloads.
"""

class SocketFailure(Exception):
    """
    Exception raised when a socket operation fails.

    This exception indicates a general failure in socket communication.
    """
    def __init__(self):
        super().__init__("Socket failure")


class MethodNotAllowed(Exception):
    """
    Exception raised when a requested HTTP method is not allowed for a resource.

    Attributes:
        allowed_methods (list): The methods that are allowed for the resource.

    Parameters:
        allowed_methods (list): A list of allowed HTTP methods.
    """
    def __init__(self, allowed_methods):
        message = f"Current method is not allowed for this resource, allowed methods: {allowed_methods}"
        super().__init__(message)


class RouteNotFound(Exception):
    """
    Exception raised when a requested route is not found.

    Attributes:
        route (str): The route that was requested but not found.

    Parameters:
        route (str): The requested route.
    """
    def __init__(self, route):
        super().__init__(f"The resource {route} you are trying to access is unavailable")


class FileNotExist(Exception):
    """
    Exception raised when a requested file does not exist.

    This exception indicates that the file requested by the client is not available.
    """
    def __init__(self):
        super().__init__("The file you are trying to access is unavailable")


class InternalServerError(Exception):
    """
    Exception raised for general internal server errors.

    Attributes:
        message (str): A message describing the error.

    Parameters:
        message (str, optional): Custom message describing the server error. Defaults to a generic message.
    """
    def __init__(self, message="Internal server error occurred"):
        super().__init__(message)


class TemplateError(Exception):
    """
    Exception raised when a template processing error occurs.

    Attributes:
        message (str): A message describing the error.
        status_code (int): HTTP status code associated with the error.

    Parameters:
        message (str, optional): Custom message describing the error. Defaults to "Invalid template".
        status_code (int, optional): HTTP status code. Defaults to 404.
    """
    def __init__(self, message="Invalid template", status_code=404):
        super().__init__(message)
        self.status_code = status_code


class SeverOverflowError(Exception):
    """
    Exception raised when the server is overloaded with excessive data.

    This exception indicates that the server is not optimized to handle the amount of data being processed.
    """
    def __init__(self):
        super().__init__("Server not optimized for this much of data")
