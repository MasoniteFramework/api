"""AuthJWTDriver Module."""

import pendulum
from masonite.auth import Auth
from masonite.contracts import AuthContract
from masonite.drivers import BaseDriver
from masonite.exceptions import DriverLibraryNotFound
from masonite.helpers import config, cookie_expire_time
from masonite.request import Request
from ..authentication import BaseAuthentication
from ..exceptions import NoApiTokenFound


class APIJwtDriver(BaseDriver, AuthContract, BaseAuthentication):

    def __init__(self, request: Request):
        """AuthCookieDriver initializer.

        Arguments:
            request {masonite.request.Request} -- The Masonite request class.
        """
        self.request = request
        try:
            import jwt
            self.jwt = jwt
        except ImportError:
            raise DriverLibraryNotFound(
                "Please install pyjwt by running 'pip install pyjwt'")

    def user(self, auth_model):
        """Gets the user based on this driver implementation

        Arguments:
            auth_model {orator.orm.Model} -- An Orator ORM type object.

        Returns:
            Model|bool
        """
        try:
            token = self.fetch_token()
        except NoApiTokenFound:
            return None

        from config.application import KEY
        from config import auth

        try:
            payload = self.jwt.decode(token, KEY, algorithms=['HS256'])
            return auth.AUTH['guards']['api']['model'].hydrate(payload['user']).first()
        except self.jwt.exceptions.DecodeError:
            self.delete()
        return False

    def save(self, _, **kwargs):
        """Saves the state of authentication.

        In this case the state is serializing the user model and saving to a token cookie.

        Arguments:
            remember_token {string} -- A token containing the state.

        Returns:
            bool
        """
        from config.application import KEY
        model = kwargs.get('model', False)
        serialized_dictionary = model.serialize()
        serialized_dictionary.update({
            'expired': cookie_expire_time('5 minutes')
        })
        token = self.jwt.encode(serialized_dictionary, KEY, algorithm='HS256')
        token = bytes(token).decode('utf-8')
        self.request.cookie('token', token)

    def delete(self):
        """Deletes the state depending on the implementation of this driver.

        Returns:
            bool
        """
        self.request.delete_cookie('token')

    def logout(self):
        self.delete()
        self.request.reset_user()
