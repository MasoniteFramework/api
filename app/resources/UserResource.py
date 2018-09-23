from api.resources import Resource
from api.serializers import JSONSerializer
from app.User import User
from api.exceptions import ApiNotAuthenticated, NoApiTokenFound
from masonite.request import Request
from api.authentication import TokenAuthentication, JWTAuthentication, PermissionScopes


class UserResource(Resource, JSONSerializer, JWTAuthentication, PermissionScopes):
    
    model = User
    without = ['password', 'plan_id', 'remember_token']
    scopes = ['user:read']

