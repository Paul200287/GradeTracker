class ExamNotFound(Exception):
    """Raised when the exam does not exist."""
    pass

class ExamAlreadyDeleted(Exception):
    """Raised when trying to access or delete an already deleted exam."""
    pass

class SubjectAccessDenied(Exception):
    """Raised when the user does not have access to the subject of the exam."""
    pass