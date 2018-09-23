from api.authentication import BaseAuthentication

class JWTAuthentication(BaseAuthentication):

    def authenticate(self):
        """Authenticate using a JWT token
        """

        if request.input('token'):
            token = request.input('token')
        elif request.header('HTTP_AUTHORIZATION'):
            token = request.header('HTTP_AUTHORIZATION').replace('Basic ', '')
        else:
            raise NoApiTokenFound

        
        Sign().unsign(token)

