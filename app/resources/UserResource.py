from api.resources import Resource
from app.User import User

class UserResource(Resource):
    
    model = User

    # def read_single(self):
    #     return {'id': 1}