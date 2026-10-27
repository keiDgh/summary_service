# Auth
class AuthError(Exception):
    pass

class UserExistsError(AuthError):
    pass

class WrongPasswordError(AuthError):
    pass

class InternalServerError(AuthError):
    pass

# Association
class UserSummaryAssociationError(Exception):
    pass

class AssociationAlreadyExistsError(UserSummaryAssociationError):
    pass

class AssociationNotFoundError(UserSummaryAssociationError):
    pass

# HTTPClient
class HTTPClientError(Exception):
    pass

class ExternalServiceTransientError(HTTPClientError):
    pass

class ExternalServiceBusinessError(HTTPClientError):
    pass

class InvalidURLError(HTTPClientError):
    pass

# Redis
class RedisError(Exception):
    pass

# Token
class TokenAuthError(Exception):
    pass

class RefreshTokenInvalidError(TokenAuthError):
    pass

class InvalidJWTError(TokenAuthError):
    pass

class InvalidAuthorizationHeader(TokenAuthError):
    pass

class ExpiredJWTError(TokenAuthError):
    pass

# ParserService
class ParserError(Exception):
    pass

class UnsupportedFileExtensionError(ParserError):
    pass

class FileNotFoundError(ParserError):
    pass

class FileDataError(ParserError):
    pass