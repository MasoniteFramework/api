from masonite.auth import Sign
from masonite.helpers.misc import random_string

class TokenController:

    def token(self):
        return {'token': Sign().sign(random_string(10))}   
