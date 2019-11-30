from src.masonite.api.resources import Resource
from src.masonite.api.filters import FilterScopes
from src.masonite.api.authentication import PermissionScopes, JWTAuthentication
from src.masonite.api.serializers import JSONSerializer
# from tests.models.User import User
from masonite.providers import RouteProvider
from masonite.routes import Route, RouteGroup
from masonite.request import Request
from masonite.response import Response
from masonite.helpers.routes import flatten_routes
import pendulum
import jwt
from config.application import KEY
from app.User import User
from masonite.testing import TestCase
from masonite.helpers import password
from src.masonite.api.routes import TokenRoutes, JWTRoutes
from masonite.auth import Auth
from src.masonite.api.guards import APIGuard

class MockJWTAuthentication(JWTAuthentication):

    def fetch_token(self):
        payload = {
            'issued': str(pendulum.now()),
            'expires': str(pendulum.now().add(minutes=1)),
            'refresh': str(pendulum.now().add(days=1)),
            'scopes': 'user:read',
        }
        return jwt.encode(payload, KEY, algorithm='HS256')


class AllUserResource(Resource, JSONSerializer, JWTAuthentication):
    model = User


class TestTokens(TestCase):

    transactions = True

    def setUp(self):
        super().setUp()
        self.auth = self.container.make(Auth)
        self.auth.register_guard('api', APIGuard)
        self.routes(only=[JWTRoutes('/token'), AllUserResource('/users').routes()])

    def setUpFactories(self):
        User.create({
            'name': 'Joe',
            'email': 'joe@email.com',
            'password': password('secret')
        })

    def test_cant_get_token_without_correct_credentials(self):
        self.json('POST', '/token').assertIsStatus(401).assertContains('error')

    def test_gets_token_with_correct_credentials(self):
        self.json('POST', '/token', {
            'username': 'joe@email.com',
            'password': 'secret'
        }).assertIsStatus(200).assertContains('token')

    def test_gets_user(self):
        self.auth.set('api')
        token = self.json('POST', '/token', {
            'username': 'joe@email.com',
            'password': 'secret'
        }).assertIsStatus(200).asDictionary()['token']

        response = self.json('GET', '/users', {'token': token}).assertCount(1)

        user = response.request.user()

        self.assertEqual(user.email, 'joe@email.com')
