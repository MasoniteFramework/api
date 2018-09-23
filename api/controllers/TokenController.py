import jwt
from masonite.auth import Sign
from masonite.helpers.misc import random_string
from config.application import KEY


class TokenController:

    def token(self):
        return {'token': Sign().sign(random_string(10))}

    def jwt(self):
        return {'token': bytes(jwt.encode({'some': 'payload'}, KEY, algorithm='HS256')).decode('utf-8')}
