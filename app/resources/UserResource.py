from masonite.request import Request

from src.api.authentication import (JWTAuthentication, PermissionScopes,
                                TokenAuthentication)
from src.api.resources import Resource
from src.api.serializers import JSONSerializer
from app.User import User
from src.api.filters import FilterScopes

class UserResource(Resource, JSONSerializer):
    model = User   
    # methods = ['create', 'index', 'show']
    scopes = ['user:read']

    def index(self, request: Request):
        return {'id': 1}