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


class TestFilterScopes(TestCase):

    def setUp(self):
        super().setUp()

    def setUpFactories(self):
        pass

    def test_filter_scopes_filters_dictionary(self):
        pass