class UserError(Exception):
    pass

class UserNotFoundError(UserError):
    pass

class UserAlreadyExistsError(UserError):
    """User with this usernme or email already exists. Database UniqueViolation"""
    pass


class SummaryError(Exception):
    pass

class SummaryNotFound(SummaryError):
    pass