class DomainError(Exception):
    """Base class for all domain-specific errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ResourceNotFoundError(DomainError):
    """Raised when a requested resource is not found."""
    pass

class InsufficientStockError(DomainError):
    """Raised when an operation fails due to insufficient stock."""
    def __init__(self, item_name: str, requested: int, available: int):
        message = f"Insufficient stock for {item_name}. Requested: {requested}, Available: {available}"
        super().__init__(message)

class DomainConflictError(DomainError):
    """Raised when an operation violates a business rule causing a conflict."""
    pass

class UnauthorizedError(DomainError):
    """Raised when an action is not permitted for the user."""
    pass

class DomainValidationError(DomainError):
    """Raised when provided data violates domain constraints."""
    pass
