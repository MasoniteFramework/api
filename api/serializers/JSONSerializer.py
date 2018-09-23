import json

class JSONSerializer:
    
    def serialize(self, response):
        """Serialize the model into JSON
        """
        return json.loads(response)