from masonite.request import Request

from api.authentication import (JWTAuthentication, PermissionScopes,
                                TokenAuthentication)
from api.resources import Resource
from api.serializers import JSONSerializer
from app.User import User
from api.filters import FilterScopes

class UserResource(Resource, JSONSerializer):
    model = User   
    # methods = ['create', 'index', 'show']
    scopes = ['user:read']

    def index(self, request: Request):
        request.status(404)
        return {'id': 1}