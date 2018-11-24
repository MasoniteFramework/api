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
                for key, value in response.items():
                    if key in self.filter_scopes[scope]:
                        filtered_response.update({key: value})

        return filtered_response
