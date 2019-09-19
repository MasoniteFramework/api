class FilterScopes:

    filter_scopes = {
        'user:read': ['name', 'email'],
        'manager': ['name',  'email', 'password']
    }

    def filter(self, response):

        if 'error' in response:
            return response

        token = self.get_token()
        scopes = token['scopes'].split(',')

        filtered_response = {}

        for scope in scopes:
            if scope in self.filter_scopes:
                if isinstance(response, dict):
                    return self.filter_dict(response, scope)
                elif isinstance(response, list):
                    return self.filter_list(response, scope)
                    
        return filtered_response

    def filter_dict(self, response, scope):
        filtered_response = {}
        for key, value in response.items():
            if key in self.filter_scopes[scope]:
                filtered_response.update({key: value})
        
        return filtered_response

    def filter_list(self, response, scope):
        filtered_response = {}
        for elem in response:
            for key, value in elem.items():
                if key in self.filter_scopes[scope]:
                    filtered_response.update({key: value})
        
        return filtered_response
