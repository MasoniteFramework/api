class ApiNotAuthenticated(Exception):
    pass


class NoApiTokenFound(Exception):
    pass


class PermissionScopeDenied(Exception):
    pass


class RateLimitReached(Exception):
    pass


class InvalidToken(Exception):
    pass


class ExpiredToken(Exception):
    pass
