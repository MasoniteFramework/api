from api.resources import Resource
from tests.models.User import User
from masonite.app import App
from masonite.providers import RouteProvider
from masonite.testsuite import TestSuite, generate_wsgi
from masonite.routes import Route
from masonite.request import Request
from masonite.view import View
from masonite.helpers.routes import flatten_routes

class ResourceTest(Resource):
    model = User
    method_type = 'GET'

    def get_response(self):
        if self.method_type == 'POST':
            # print('getting method:', 'create')
            return self.request.app().resolve(getattr(self, 'create'))
        elif self.method_type == 'GET' and '@' in self.route_url:
            # print('getting method:', 'read_single')
            return self.request.app().resolve(getattr(self, 'read_single'))
        elif self.method_type == 'GET':
            # print('getting method:', 'read')
            return self.request.app().resolve(getattr(self, 'read'))
        elif self.method_type == 'PUT':
            # print('getting method:', 'update')
            return self.request.app().resolve(getattr(self, 'update'))
        elif self.method_type == 'DELETE':
            # print('getting method:', 'delete')
            return self.request.app().resolve(getattr(self, 'delete'))
        
    def create(self):
        return 'create'

    def read(self):
        return 'read'

    def read_single(self):
        return 'read_single'

    def update(self):
        return 'update'

    def delete(self):
        return 'delete'

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
        self.app.bind('Headers', [])
        self.app.bind('StatusCode', '404 Not Found')
        self.app.bind('HttpMiddleware', [])
        view = View(self.app)
        self.app.bind('ViewClass', view)
        self.app.bind('View', view.render)
        self.provider = RouteProvider()
        self.provider.app = self.app
        
    def test_resource_can_return_response_acting_as_route(self):
        self.app.make('Route').url = '/api/1'
        self.app.make('Request').path = '/api/1'
        self.app.bind('WebRoutes', [ResourceTest('/api')])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request')
        )

        assert self.app.make('Response') == 'read_single'

    def test_resource_returns_correct_routes(self):
        routes = ResourceTest('/api').routes()

        assert len(routes) == 5

    def test_resource_can_return_response_acting_as_route(self):
        self.app.make('Route').url = '/api/1'
        self.app.make('Request').path = '/api/1'
        self.app.bind('WebRoutes', ResourceTest('/api').routes())

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request')
        )

        assert self.app.make('Response') == 'read_single'

    def test_output_routes(self):
        for route in ResourceTest('/api').routes():
            print(route.route_url, route.method_type)

