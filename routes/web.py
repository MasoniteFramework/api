""" Web Routes """
from masonite.routes import Get, Post

from src.api.routes import JWTRoutes, TokenRoutes
from app.resources.UserResource import UserResource

ROUTES = [
    Get().route('/', 'WelcomeController@show').name('welcome'),
    UserResource('/api/user').routes(),

    TokenRoutes('/token'),
    JWTRoutes('/authorize'),
]
