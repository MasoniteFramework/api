from api.resources import Resource
from tests.models.User import User
from masonite.app import App
from masonite.providers import RouteProvider
from masonite.testsuite import TestSuite, generate_wsgi
from masonite.routes import Route
from masonite.request import Request
from masonite.view import View

class ResourceTest(Resource):
    model = User
    method_type = 'GET'

    def get_response(self):
        return 'test'

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
        
    def test_resource_can_return_response_as_route(self):
        self.app.make('Route').url = '/view'
        self.app.bind('WebRoutes', [ResourceTest('/view')])

        self.provider.boot(
            self.app.make('Route'),
            self.app.make('Request')
        )

        assert self.app.make('Response') == 'test'
