""" Web Routes """
from masonite.routes import Get, Post
from app.resources.UserResource import UserResource

ROUTES = [
    Get().route('/', 'WelcomeController@show').name('welcome'),
    UserResource('/api').routes(),
]
