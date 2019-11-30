from masonite.request import Request

from src.masonite.api.authentication import (JWTAuthentication, PermissionScopes,
                                TokenAuthentication)
from src.masonite.api.resources import Resource
from src.masonite.api.serializers import JSONSerializer
from app.User import User
from src.masonite.api.filters import FilterScopes

class UserResource(Resource, JSONSerializer):
    model = User   
    # methods = ['create', 'index', 'show']
    scopes = ['user:read']

    def index(self, request: Request):
        return {'id': 1}