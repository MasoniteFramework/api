class Resource:
    """Resource class that will use a similar structure as a Route class.
    """
    
    model = None
    methods = ['create', 'read', 'read_single', 'update', 'delete']
    prefix = '/api'
    method_routes = {
        'create': '', # POST request
        'read': '', # GET request
        'read_single': '/@id',
        'update': '/@id',
        'delete': '/@id',
    }

    def __init__(self, url=None, method_type='GET'):
        self.route_url = url
        self.method_type = method_type

    def routes(self):
        routes = []
        for method in self.methods:
            if method == 'create':
                routes.append(self.__class__(self.route_url, 'POST'))
            elif method == 'read':
                routes.append(self.__class__(self.route_url, 'GET'))
            elif method == 'read_single':
                routes.append(self.__class__(self.route_url + '/@id', 'GET'))
            elif method == 'update':
                routes.append(self.__class__(self.route_url + '/@id', 'PUT'))
            elif method == 'delete':
                routes.append(self.__class__(self.route_url + '/@id', 'DELETE'))
        
        return routes
    
    def get_response(self):
        """Gets the response that should be returned from this resource
        """
        if self.method_type == 'POST':
            return self.request.app().resolve(getattr(self, 'create'))
        elif self.method_type == 'GET' and '@' in self.route_url:
            return self.request.app().resolve(getattr(self, 'read_single'))
        elif self.method_type == 'GET':
            return self.request.app().resolve(getattr(self, 'read'))
        elif self.method_type == 'PUT':
            return self.request.app().resolve(getattr(self, 'update'))
        elif self.method_type == 'DELETE':
            return self.request.app().resolve(getattr(self, 'delete'))

    
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
        pass
        
    def read(self): 
        """Logic to read data from a given model
        """
        pass

    def update(self): 
        """Logic to update data from a given model
        """
        pass

    def delete(self): 
        """Logic to delete data from a given model
        """
        pass
