from api.authentication import BaseAuthentication
from api.exceptions import NoApiTokenFound
import jwt
from config.application import KEY
from masonite.request import Request
import pendulum

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request: Request):
        """Authenticate using a JWT token
        """

        if request.input('token'):
            token = request.input('token')
        elif request.header('HTTP_AUTHORIZATION'):
            token = request.header('HTTP_AUTHORIZATION').replace('Basic ', '')
        else:
            raise NoApiTokenFound

        token = jwt.decode(token, KEY, algorithms=['HS256'])
        print(pendulum.parse(token['expires']).is_past())
        print(token)
