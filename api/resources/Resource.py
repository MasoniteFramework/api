class Resource:
    """Resource class that will use a similar structure as a Route class.
    """
    
    model = None

    def __init__(self):
        self.route_url = None
    
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
    
    def compile_route_to_regex(self):
        """Compiles this resource url to a regex pattern
        """
        pass

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
