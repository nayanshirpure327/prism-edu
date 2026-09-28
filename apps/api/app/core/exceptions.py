from fastapi import status

class PrismException(Exception):
    def __init__(self, message: str, status_code: int = 400, error_code: str = "BAD_REQUEST", details: dict = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

class AuthenticationError(PrismException):
    def __init__(self, message="Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, "AUTH_ERROR")

class AuthorizationError(PrismException):
    def __init__(self, message="Not authorized"):
        super().__init__(message, status.HTTP_403_FORBIDDEN, "FORBIDDEN")

class NotFoundError(PrismException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND, "NOT_FOUND")

class ValidationError(PrismException):
    def __init__(self, message="Validation error", details=None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR", details)

class ConflictError(PrismException):
    def __init__(self, message="Resource conflict"):
        super().__init__(message, status.HTTP_409_CONFLICT, "CONFLICT")

class ExternalServiceError(PrismException):
    def __init__(self, message="External service error"):
        super().__init__(message, status.HTTP_502_BAD_GATEWAY, "EXTERNAL_SERVICE_ERROR")

class RateLimitError(PrismException):
    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message, status.HTTP_429_TOO_MANY_REQUESTS, "RATE_LIMIT_ERROR")
