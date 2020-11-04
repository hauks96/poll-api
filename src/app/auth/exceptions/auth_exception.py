class InvalidUserCreation(Exception):
    pass


class AuthenticationFailed(Exception):
    pass


class AuthRelationCreationFailed(Exception):
    pass


class AuthRelationDeletionFailed(Exception):
    pass


class VoteFailed(Exception):
    pass


class CreationLimitReached(Exception):
    pass
