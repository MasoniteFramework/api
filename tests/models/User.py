from orator import Model
class User(Model):

    id = 1
    name = 'Test User'
    email = 'test@email.com'

    @staticmethod
    def find(id):
        user = User()
        user.id = 1
        user.name = 'Test User'
        user.email = 'test@email.com'
        return user
    
    def serialize(self):
        return {'id': 1}
