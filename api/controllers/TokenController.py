import jwt
from masonite.auth import Sign
from masonite.request import Request
from masonite.helpers.misc import random_string
from config.application import KEY
import pendulum


class TokenController:

    def token(self):
        return {'token': Sign().sign(random_string(10))}

    def jwt(self, request: Request):
        payload = {
            'issued': str(pendulum.now()),
            'expires': str(pendulum.now().add(minutes=5)),
            'scopes': request.input('scopes'),
        }
        print('payload')
        return {'token': bytes(jwt.encode(payload, KEY, algorithm='HS256')).decode('utf-8')}
