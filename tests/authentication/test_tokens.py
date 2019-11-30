from masonite.auth import Auth
from masonite.helpers import password
from masonite.testing import TestCase

from app.User import User
from src.masonite.api.authentication import JWTAuthentication
from src.masonite.api.filters import FilterScopes
from src.masonite.api.resources import Resource
from src.masonite.api.routes import JWTRoutes, TokenRoutes
from src.masonite.api.serializers import JSONSerializer



class AllUserResource(Resource, JSONSerializer, JWTAuthentication):
    model = User


class TestTokens(TestCase):

    transactions = True

    def setUp(self):
        super().setUp()
        self.auth = self.container.make(Auth)
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
        }).assertIsStatus(200).assertContains('token').assertContains('expires_at').assertContains('refresh_expires_at')

    def test_gets_user(self):
        self.auth.set('api')
        token = self.json('POST', '/token', {
            'username': 'joe@email.com',
            'password': 'secret'
        }).assertIsStatus(200).asDictionary()['token']

        response = self.json('GET', '/users', {'token': token}).assertCount(1)

        user = response.request.user()

        self.assertEqual(user.email, 'joe@email.com')
