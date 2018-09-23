from api.resources import Resource
from api.serializers import JSONSerializer
from app.User import User
from api.exceptions import ApiNotAuthenticated, NoApiTokenFound
from masonite.request import Request
from api.authentication import TokenAuthentication, JWTAuthentication, PermissionScopes


class UserResource(Resource, JSONSerializer, JWTAuthentication, PermissionScopes):
    
    model = User
    without = ['password', 'plan_id', 'remember_token']
    scopes = ['user:read', 'user:create']

    # def authenticate(self, request: Request):
    #     if request.input('token'):
    #         token = request.input('token')
    #     elif request.header('HTTP_AUTHORIZATION'):
    #         token = request.header('HTTP_AUTHORIZATION').replace('Basic ', '')
    #     else:
    #         raise NoApiTokenFound
        
    #     if not token == '1234':
    #         raise ApiNotAuthenticated
