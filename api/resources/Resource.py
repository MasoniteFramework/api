import json
from masonite.request import Request

class Resource:
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

    def routes(self):
        routes = []
        for method in self.methods:
            if method == 'create':
                routes.append(self.__class__(self.route_url, 'POST'))
            elif method == 'index':
                routes.append(self.__class__(self.route_url, 'GET'))
            elif method == 'show':
                routes.append(self.__class__(self.route_url + '/@id', 'GET'))
            elif method == 'update':
                routes.append(self.__class__(self.route_url + '/@id', 'PUT'))
            elif method == 'delete':
                routes.append(self.__class__(self.route_url + '/@id', 'DELETE'))
        
        return routes
    
    def get_response(self):
        """Gets the response that should be returned from this resource
        """

        response = None

        if hasattr(self, 'authenticate'):
            # Get a response from the authentication method if one exists
            response = self.request.app.resolve(self.authenticate())

        # If the authenticate method did not return a response, continue on to one of the CRUD responses
        if not response:
            if self.method_type == 'POST':
                response = self.request.app().resolve(getattr(self, 'create'))
            elif self.method_type == 'GET' and '@' in self.route_url:
                response = self.request.app().resolve(getattr(self, 'index'))
            elif self.method_type == 'GET':
                response = self.request.app().resolve(getattr(self, 'show'))
            elif self.method_type == 'PUT':
                response = self.request.app().resolve(getattr(self, 'update'))
            elif self.method_type == 'DELETE':
                response = self.request.app().resolve(getattr(self, 'delete'))

        # If the resource needs it's own serializer method
        if hasattr(self, 'serialize'):
            response = self.serialize(response)

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
    
    def compile_route_to_regex(self, router):
        """Compiles this resource url to a regex pattern
        """

        # Split the route
        split_given_route = self.route_url.split('/')
        # compile the provided url into regex
        url_list = []
        regex = '^'
        for regex_route in split_given_route:
            if '@' in regex_route:
                if ':' in regex_route:
                    try:
                        regex += router.route_compilers[regex_route.split(':')[
                            1]]
                    except KeyError:
                        raise InvalidRouteCompileException(
                            'Route compiler "{}" is not an available route compiler. '
                            'Verify you spelled it correctly or that you have added it using the compile() method.'.format(
                                regex_route.split(':')[1])
                        )
                else:
                    regex += router.route_compilers['default']

                regex += r'\/'

                # append the variable name passed @(variable):int to a list
                url_list.append(
                    regex_route.replace('@', '').split(':')[0]
                )
            else:
                regex += regex_route + r'\/'

        router.url_list = url_list
        regex += '$'
        return regex

    def create(self): 
        """Logic to create data from a given model
        """
        try:
            record = self.model.create(self.request.all())
        except Exception as e:
            return {'error': str(e)}
        return record
        
    def index(self, request: Request): 
        """Logic to read data from a given model
        """
        return self.model.find(request.param('id'))

    def show(self): 
        """Logic to read data from a given model
        """
        return self.model.all()

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
            print('returning record')
            return record

        return {'error': 'Model does not exist'}
        
