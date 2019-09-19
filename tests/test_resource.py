from src.api.resources import Resource
from masonite.routes import RouteGroup
from masonite.request import Request
from masonite.testing import TestCase
from app.User import User
from masonite.helpers import password


class ResourceTest(Resource):
    model = User
    method_type = 'GET'

    def show(self, request: Request):
        request.status(203)
        return 'read_single'


class ResourceJsonTest(Resource):
    model = User
    method_type = 'GET'

    def index(self, request: Request):
        return {'id': 1}


class TestResource(TestCase):

    def setUp(self):
        super().setUp()
        self.routes(ResourceTest('/api').routes())

    def setUpFactories(self):
        User.create({
            'name': 'Joe',
            'email': 'Joe@email.com',
            'password': password('secret')
        })

    def test_resource_can_return_response_acting_as_route(self):
        self.assertTrue(self.json('GET', '/api/1').hasJson('name', 'Joe'))

    def test_resource_returns_correct_routes(self):
        routes = ResourceTest('/api').routes()

        assert len(routes) == 5

    def test_resource_middleware_returns_json_from_dictionary(self):
        self.routes(ResourceJsonTest('/api/json').routes())
        self.assertTrue(self.json('GET', '/api/json/1').hasJson('id', 1))

    def test_route_groups_middleware(self):
        group = RouteGroup([
            ResourceJsonTest('/api').routes()
        ], middleware=('auth',))

        assert group[0].list_middleware == ['auth']
