from masonite.auth import Sign
from masonite.request import Request

from ..authentication import BaseAuthentication
from ..exceptions import ApiNotAuthenticated, NoApiTokenFound


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request: Request):
        """Authentication using Signed tokens

        Returns:
            None -- Should return None if a successful authentication or an exception if not.
        """

        try:
            self.get_token()
        except Exception:
            raise ApiNotAuthenticated

    def get_token(self):
        """Returns the decrypted string as a dictionary. This method needs to be overwritten on each authentication class.

        Returns:
            dict -- Should always return a dictionary
        """

        return Sign().unsign(self.fetch_token())
