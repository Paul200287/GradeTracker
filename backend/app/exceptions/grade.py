class GradeNotFound(Exception):
    """Raised when the requested grade does not exist."""
    pass

class GradeAccessDenied(Exception):
    """Raised when the user does not have permission to access or modify the grade."""
    pass

class InvalidGradeData(Exception):
    """Raised when grade data is invalid or violates constraints."""
    pass
