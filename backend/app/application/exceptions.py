class UserSummaryAssociationError(Exception):
    pass

class AssociationAlreadyExistsError(UserSummaryAssociationError):
    pass

class AssociationNotFoundError(UserSummaryAssociationError):
    pass