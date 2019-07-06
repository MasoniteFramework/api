from api.authentication import BaseAuthentication
from api.exceptions import NoApiTokenFound, ExpiredToken, InvalidToken
import jwt
from config.application import KEY
from masonite.request import Request
import pendulum

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request: Request):
        """Authenticate using a JWT token
        """
        token = self.get_token()
        if pendulum.parse(token['expires']).is_past():
            raise ExpiredToken

    def get_token(self):
        """Returns the decrypted string as a dictionary. This method needs to be overwritten on each authentication class.
        
        Returns:
            dict -- Should always return a dictionary
        """

        try:
            return jwt.decode(self.fetch_token(), KEY, algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            raise InvalidToken
