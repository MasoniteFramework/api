from api.resources import Resource
from api.filters import FilterScopes
from api.authentication import PermissionScopes, JWTAuthentication
from api.serializers import JSONSerializer
# from tests.models.User import User
from masonite.providers import RouteProvider
from masonite.testsuite import TestSuite, generate_wsgi
from masonite.routes import Route, RouteGroup
from masonite.request import Request
from masonite.response import Response
from masonite.helpers.routes import flatten_routes
import pendulum
import jwt
from config.application import KEY
from app.User import User


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

class TestFilterScopes:

    def setup_method(self):
        from wsgi import container
        self.app = container
        self.app.make('Request').environ = generate_wsgi()
        self.app.make('Request').load_app(self.app)
        self.app.bind('StatusCode', None)
        self.provider = RouteProvider()
        self.provider.app = self.app

    def test_filter_scopes_filters_dictionary(self):
        self.app.make('Route').url = '/api'
        request = self.app.make('Request')
        request.request_variables = {}
        request.path = '/api/1'
        self.app.bind('WebRoutes', UserResourceTest('/api').routes())

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response),
        )

        assert '"name":' in self.app.make('Response')
        assert '"email":' in self.app.make('Response')
        assert '"id":' not in self.app.make('Response')
