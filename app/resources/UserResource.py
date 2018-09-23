from api.resources import Resource
from api.serializers import JSONSerializer
from app.User import User

class UserResource(Resource, JSONSerializer):
    
    model = User
    without = ['password', 'plan_id', 'remember_token']

