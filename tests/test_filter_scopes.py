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


class MockJWTAuthentication(JWTAuthentication):

    def fetch_token(self):
        payload = {
            'issued': str(pendulum.now()),
            'expires': str(pendulum.now().add(minutes=1)),
            'refresh': str(pendulum.now().add(days=1)),
            'scopes': 'user:read',
        }
        return jwt.encode(payload, KEY, algorithm='HS256')


class UserResourceTest(Resource, JSONSerializer, MockJWTAuthentication, PermissionScopes, FilterScopes):
    model = User
    scopes = ['user:read']
    filter_scopes = {
        'user:read': ['name', 'email'],
        'user:manager': ['id', 'name', 'email', 'active', 'password']
    }

    def show(self):
        return {
            'name': 'Joe',
            'email': 'test@email.com',
            'active': 1,
            'password': '1234'
        }

    def index(self):
        return self.model.all()


class TestFilterScopes(TestCase):

    transactions = True

    def setUp(self):
        super().setUp()
        self.routes(UserResourceTest('/api').routes())

    def setUpFactories(self):
        User.create({
            'name': 'Joe',
            'email': 'joe@email.com',
            'password': password('secret')
        })

    def test_filter_scopes_filters_dictionary(self):
        self.assertTrue(self.json('GET', '/api/1').contains('name'))
        self.assertTrue(self.json('GET', '/api/1').contains('email'))
        self.assertFalse(self.json('GET', '/api/1').contains('id'))
