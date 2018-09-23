from api.resources import Resource
from app.User import User

class UserResource(Resource):
    
    model = User
    without = ['password', 'plan_id', 'remember_token']

    # def read_single(self):
    #     return {'id': 1}
