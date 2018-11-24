from masonite.request import Request

from api.authentication import (JWTAuthentication, PermissionScopes,
                                TokenAuthentication)
from api.resources import Resource
from api.serializers import JSONSerializer
from app.User import User
from api.filters import ScopeFilter

class UserResource(Resource, JSONSerializer, JWTAuthentication, PermissionScopes, ScopeFilter):
    model = User   
    # methods = ['create', 'index', 'show']
    scopes = ['user:read']