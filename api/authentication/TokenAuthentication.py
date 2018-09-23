from api.authentication import BaseAuthentication
from masonite.auth import Sign
from api.exceptions import NoApiTokenFound, ApiNotAuthenticated
from masonite.request import Request

class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request: Request):
        """Authentication using Signed tokens
        """

        if request.input('token'):
            token = request.input('token')
        elif request.header('HTTP_AUTHORIZATION'):
            token = request.header('HTTP_AUTHORIZATION').replace('Basic ', '')
        else:
            raise NoApiTokenFound

        try:
            Sign().unsign(token)
        except Exception as e:
            raise ApiNotAuthenticated
