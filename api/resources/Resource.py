class Resource:
    """Resource class that will use a similar structure as a Route class.
    """
    
    model = None

    def __init__(self, url=None):
        self.route_url = url
    
    def get_response(self):
        """Gets the response that should be returned from this resource
        """
        pass
    
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
