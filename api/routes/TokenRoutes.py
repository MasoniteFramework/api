from masonite.routes import Get, Post
from api.controllers import TokenController


def TokenRoutes(url='/token'):
    return [
        Get().route(url, TokenController.token)
    ]

def JWTRoutes(url='/jwt', auth=None):
    controller = TokenController
    controller.__auth__ = auth
    return [
        Post().route(url, controller.jwt),
        Post().route(url + '/refresh', controller.jwt_refresh),
    ]

