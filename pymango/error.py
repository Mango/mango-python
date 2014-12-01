"""
Mango Library Exceptions
"""


class MangoException(Exception):
    """Base exception"""
    pass


class InvalidApiKey(MangoException):
    """Invalid API Key"""
    pass


class UnableToConnect(MangoException):
    """Unable to connect into Mango API"""
    pass


class NotFound(MangoException):
    """Resource not found"""
    pass


class MethodNotAllowed(MangoException):
    """Method not allowed"""
    pass


class AuthenticationError(MangoException):
    """Authentication error"""
    pass


class UnhandledError(MangoException):
    """Unhandled error"""
    pass


class InputValidationError(MangoException):
    """Input validation error"""
    def __init__(self, error_code, error_message):
        self.code = error_code
        self.message = error_message

    def __str__(self):
        return repr("{code}: {message}".format(
            code=self.code,
            message=self.message
        ))


class InputValidationGenericError(MangoException):
    """Input validation generic error"""
    pass