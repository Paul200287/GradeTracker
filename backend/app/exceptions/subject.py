class SubjectNotFound(Exception):
    """Raised when the requested subject does not exist."""
    pass

class PermissionDenied(Exception):
    """Raised when the user does not have permission to access or modify the subject."""
    pass

class SubjectAlreadyDeleted(Exception):
    """Raised when trying to delete a subject that is already marked as deleted."""
    pass

class InvalidSubjectOwner(Exception):
    """Raised when a non-superuser tries to create a subject for another user."""
    pass