import json
from orator.support.collection import Collection
from orator import Model


class JSONSerializer:

    def serialize(self, response):
        """Serialize the model into JSON
        """
        if isinstance(response, Collection):
            return response.serialize()
        elif isinstance(response, Model):
            return response.to_dict()

        return response
