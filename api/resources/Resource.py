import json

from masonite.request import Request
from masonite.routes import BaseHttpRoute

from api.exceptions import (ApiNotAuthenticated, ExpiredToken, InvalidToken,
                            NoApiTokenFound, PermissionScopeDenied,
                            RateLimitReached)


class Resource(BaseHttpRoute):
    """Resource class that will use a similar structure as a Route class.
    """

    model = None
    methods = ['create', 'index', 'show', 'update', 'delete']
    prefix = '/api'
    required_domain = None
    list_middleware = []
    without = []

    def __init__(self, url=None, method_type='GET'):
        self.route_url = url
        self.method_type = method_type
        self.named_route = None
        self.model.__hidden__ = self.without
        if url and method_type:
            self._compiled_url = self.compile_route_to_regex()

    def routes(self):
        routes = []
        if 'create' in self.methods:
            routes.append(self.__class__(self.route_url, 'POST'))
        if 'index' in self.methods:
            routes.append(self.__class__(self.route_url, 'GET'))
        if 'show' in self.methods:
            routes.append(self.__class__(self.route_url + '/@id', 'GET'))
        if 'update' in self.methods:
            routes.append(self.__class__(self.route_url + '/@id', 'PUT'))
        if 'delete' in self.methods:
            routes.append(self.__class__(self.route_url + '/@id', 'DELETE'))

        return routes

    def get_response(self):
        """Gets the response that should be returned from this resource
        """

        response = None

        if hasattr(self, 'authenticate'):
            # Get a response from the authentication method if one exists
            response = self.run_authentication()

        if hasattr(self, 'scope'):
            # Get a response from the authentication method if one exists
            if not response:
                response = self.run_scope()

        # If the authenticate method did not return a response, continue on to one of the CRUD responses
        if not response:
            if 'POST' in self.method_type:
                response = self.request.app().resolve(getattr(self, 'create'))
            elif 'GET' in self.method_type and '@' in self.route_url:
                response = self.request.app().resolve(getattr(self, 'show'))
            elif 'GET' in self.method_type:
                response = self.request.app().resolve(getattr(self, 'index'))
            elif 'PUT' in self.method_type or 'PATCH' in self.method_type:
                response = self.request.app().resolve(getattr(self, 'update'))
            elif 'DELETE' in self.method_type:
                response = self.request.app().resolve(getattr(self, 'delete'))

        # If the resource needs it's own serializer method
        if hasattr(self, 'serialize'):
            response = self.serialize(response)
        # If the resource needs it's own serializer method
        if hasattr(self, 'filter'):
            response = self.filter(response)

        return response

    def run_middleware(self, middleware_type):
        """Runs any middleware necessary for this resource

        Arguments:
            middleware_type {string} -- Either 'before' or 'after'
        """
        pass

    def load_request(self, request):
        self.request = request
        return self

    def create(self):
        """Logic to create data from a given model
        """
        try:
            record = self.model.create(self.request.all())
        except Exception as e:
            return {'error': str(e)}
        return record

    def index(self):
        """Logic to read data from several models
        """
        return self.model.all()

    def show(self, request: Request):
        """Logic to read data from 1 model
        """
        return self.model.find(request.param('id'))

    def update(self, request: Request):
        """Logic to update data from a given model
        """
        record = self.model.find(request.param('id'))
        record.update(request.all())
        return record

    def delete(self, request: Request):
        """Logic to delete data from a given model
        """
        record = self.model.find(request.param('id'))
        if record:
            record.delete()
            return record

        return {'error': 'Record does not exist'}
