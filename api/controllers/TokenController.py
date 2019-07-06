import jwt
import pendulum
from masonite.auth import Auth, Sign
from masonite.helpers import password as bcrypt_password
from masonite.helpers.misc import random_string
from masonite.request import Request

from api.exceptions import NoApiTokenFound
from config.application import KEY


class TokenController:

    """Placeholder for the authentication model. This is set via the corresponding TokenRoutes function.
    This will default to the auth.py authentication class.
    """

    __auth__ = None

    def __init__(self):
        if self.__auth__ == None:
            from config import auth
            self.__auth__ = auth.AUTH['model']

    def token(self):
        return {'token': Sign().sign(random_string(10))}

    def jwt(self, request: Request, auth: Auth):
        if not request.input('username') or not request.input('password'):
            return {'error': 'missing username or password'}

        if auth.once().login(
            request.input('username'),
            request.input('password'),
        ):
            payload = {
                'issued': str(pendulum.now()),
                'expires': str(pendulum.now().add(minutes=1)),
                'refresh': str(pendulum.now().add(days=1)),
                'scopes': request.input('scopes'),
            }
            
            return {'token': bytes(jwt.encode(payload, KEY, algorithm='HS256')).decode('utf-8')}

        return {'error': 'invalid authentication credentials'}

    def jwt_refresh(self, request: Request):
        try:
            token = jwt.decode(self.fetch_token(request), KEY, algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            return {'error': 'invalid JWT token'}

        if not pendulum.parse(token['refresh']).is_past():
            payload = {
                'issued': str(pendulum.now()),
                'expires': str(pendulum.now().add(minutes=5)),
                'refresh': str(pendulum.now().add(days=1)),
                'scopes': token['scopes'],
            }

            return {'token': bytes(jwt.encode(payload, KEY, algorithm='HS256')).decode('utf-8')}

        return {'error': 'the refresh key on the jwt token has expired'}

    def fetch_token(self, request):
        """Gets the token from the request object

        Raises:
            NoApiTokenFound -- Raised if no API token can be located

        Returns:
            string -- Returns the token as a string
        """

        if request.input('token'):
            token = request.input('token')
        elif request.header('HTTP_AUTHORIZATION'):
            token = request.header(
                'HTTP_AUTHORIZATION').replace('Basic ', '')
        else:
            raise NoApiTokenFound

        return token
