""" Web Routes """
from masonite.routes import Get, Post
from app.resources.UserResource import UserResource
from api.routes import TokenRoutes, JWTRoutes

ROUTES = [
    Get().route('/', 'WelcomeController@show').name('welcome'),
    UserResource('/api/user').routes(),
    TokenRoutes('/token'),
    JWTRoutes('/jwt'),
]

ROUTES = ROUTES + [
    Get().route('/login', 'LoginController@show'),
    Get().route('/logout', 'LoginController@logout'),
    Post().route('/login', 'LoginController@store'),
    Get().route('/register', 'RegisterController@show'),
    Post().route('/register', 'RegisterController@store'),
    Get().route('/home', 'HomeController@show'),
]
