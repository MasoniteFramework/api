from api.authentication import BaseAuthentication
from masonite.auth import Sign
from api.exceptions import NoApiTokenFound, ApiNotAuthenticated
from masonite.request import Request

class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request: Request):
        """Authentication using Signed tokens

        Returns:
            None -- Should return None if a successful authentication or an exception if not.
        """

        try:
            self.get_token()
        except Exception as e:
            raise ApiNotAuthenticated

    def get_token(self):
        """Returns the decrypted string as a dictionary. This method needs to be overwritten on each authentication class.
        
        Returns:
            dict -- Should always return a dictionary
        """
        
        return Sign().unsign(self.fetch_token())
