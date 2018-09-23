from masonite.routes import Get, Post
from api.controllers import TokenController


def TokenRoutes(url='/token'):
    return [
        Get().route(url, TokenController.token)
    ]

def JWTRoutes(url='/jwt'):
    return [
        Post().route(url, TokenController.jwt),
        Post().route(url + '/refresh', TokenController.jwt_refresh),
    ]

