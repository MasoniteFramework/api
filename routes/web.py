""" Web Routes """
from masonite.routes import Get, Post

from api.routes import JWTRoutes, TokenRoutes
from app.resources.UserResource import UserResource

ROUTES = [
    Get().route('/', 'WelcomeController@show').name('welcome'),
    UserResource('/api/user').routes(),

    TokenRoutes('/token'),
    JWTRoutes('/authorize'),
]

ROUTES = ROUTES + [
    Get().route('/login', 'LoginController@show'),
    Get().route('/logout', 'LoginController@logout'),
    Post().route('/login', 'LoginController@store'),
    Get().route('/register', 'RegisterController@show'),
    Post().route('/register', 'RegisterController@store'),
    Get().route('/home', 'HomeController@show'),
]
