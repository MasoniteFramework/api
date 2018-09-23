from api.exceptions import (ApiNotAuthenticated, ExpiredToken, InvalidToken,
                            NoApiTokenFound, PermissionScopeDenied,
                            RateLimitReached)


class BaseAuthentication:

    def run_authentication(self):
        """Call the authenticate method and check for any exceptions thrown

        Returns:
            None|dict -- Should return None if a successful authentication or a dictionary with an error if not successfully authenticated
        """

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
            raise e
            return {'error': str(e)}

    def fetch_token(self):
        """Gets the token from the request object

        Raises:
            NoApiTokenFound -- Raised if no API token can be located

        Returns:
            string -- Returns the token as a string
        """

        if self.request.input('token'):
            token = self.request.input('token')
        elif self.request.header('HTTP_AUTHORIZATION'):
            token = self.request.header(
                'HTTP_AUTHORIZATION').replace('Basic ', '')
        else:
            raise NoApiTokenFound

        return token
