from api.resources import Resource
from tests.models.User import User
from masonite.app import App
from masonite.providers import RouteProvider
from masonite.testsuite import TestSuite, generate_wsgi
from masonite.routes import Route, RouteGroup
from masonite.request import Request
from masonite.view import View
from masonite.helpers.routes import flatten_routes
from config import middleware
from masonite.auth import Csrf
from masonite.response import Response

class ResourceTest(Resource):
    model = User
    method_type = 'GET'

    def show(self):
        return 'read_single'

class ResourceJsonTest(Resource):
    model = User
    method_type = 'GET'

    def index(self):
        return {'id': 1}

class Application:
    DEBUG = True

class TestResource:
    
    def setup_method(self):
        self.app = App()
        self.app.bind('Container', self.app)
        self.app.bind('Environ', generate_wsgi())
        self.app.bind('Application', Application)
        self.app.bind('WebRoutes', [])
        self.app.bind('Route', Route(self.app.make('Environ')))
        self.app.bind('Request', Request(
            self.app.make('Environ')).load_app(self.app))
        self.app.simple(Response(self.app))
        self.app.bind('Headers', [])
        self.app.bind('Csrf', Csrf(self.app.make('Request')))
        self.app.bind('StatusCode', '404 Not Found')
        self.app.bind('HttpMiddleware', middleware.HTTP_MIDDLEWARE)
        view = View(self.app)
        self.app.bind('ViewClass', view)
        self.app.bind('View', view.render)
        self.provider = RouteProvider()
        self.provider.app = self.app
        
    def test_resource_can_return_response_acting_as_route(self):
        self.app.make('Route').url = '/api/1'
        self.app.make('Request').path = '/api/1'
        self.app.bind('WebRoutes', ResourceTest('/api').routes())

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response),
        )

        assert self.app.make('Response') == 'read_single'

    def test_resource_returns_correct_routes(self):
        routes = ResourceTest('/api').routes()

        assert len(routes) == 5

    def test_resource_middleware_returns_json_from_dictionary(self):
        self.app.make('Route').url = '/api/1'
        self.app.make('Request').path = '/api/1'
        self.app.bind('WebRoutes', ResourceJsonTest('/api').routes())

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request'),
            self.app.make(Response),
        )

        assert self.app.make('Response') == '{"id": 1}'

    def test_output_routes(self):
        for route in ResourceTest('/api').routes():
            pass
            # print(route.route_url, route.method_type)


    def test_route_groups_middleware(self):
        group = RouteGroup([
            ResourceJsonTest('/api').routes()
        ], middleware=('auth',))

        assert group[0].list_middleware == ['auth']
