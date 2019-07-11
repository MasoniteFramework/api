from api.resources import Resource
from api.authentication import JWTAuthentication
from masonite.routes import RouteGroup
from masonite.request import Request
from masonite.testing import TestCase
from app.User import User
from masonite.helpers import password
from api.routes import JWTRoutes
import json


class ResourceTest(Resource, JWTAuthentication):
    model = User

class TestJwtToken(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(JWTRoutes('/token') + ResourceTest('/api').routes())

    def setUpFactories(self):
        User.create({
            'name': 'Joe',
            'email': 'Joe@email.com',
            'password': password('secret')
        })
        
    def test_can_authenticate(self):
        token = json.loads(self.post('/token', {'username': 'Joe@email.com', 'password': 'secret'}).container.make('Response'))['token']
        print(self.get('/api/1', {'token': token}).container.make('Response'))

    def test_can_get_token(self):
        self.assertTrue(self.post('/token').hasJson('error'))
        self.assertTrue(self.post('/token', {'username': 'Joe@email.com', 'password': 'secret'}).hasJson('token'))

