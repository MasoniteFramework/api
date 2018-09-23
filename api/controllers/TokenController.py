from masonite.auth import Sign

class TokenController:

    def token(self):
        return {'token': Sign().sign('12345')}   
