from api.exceptions import (ApiNotAuthenticated, ExpiredToken, InvalidToken,
                            NoApiTokenFound, PermissionScopeDenied,
                            RateLimitReached)

class BaseAuthentication:

    def run_authentication(self):
        try:
            return self.request.app().resolve(self.authenticate)
        except ApiNotAuthenticated:
            return {'error': 'token not authenticated'}
        except ExpiredToken:
            return {'error': 'token has expired'}
        except InvalidToken:
            return {'error': 'token is invalid'}
        except NoApiTokenFound:
            return {'error': 'no API token found'}
        except PermissionScopeDenied:
            return {'error': 'token has invalid scope permissions'}
        except RateLimitReached:
            return {'error': 'rate limit reached'}
        except Exception as e:
            return {'error': str(e)}
