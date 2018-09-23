from api.exceptions import PermissionScopeDenied

class PermissionScopes:

    scopes = ['*']

    def scope(self):
        token = self.get_token()
        if 'scopes' not in token or not set(token['scopes'].split(',')).issubset(self.scopes) or self.scopes == ['*']:
            raise PermissionScopeDenied

    def run_scope(self, scopes: list):
        try:
            return self.scope()
        except PermissionScopeDenied:
            return {'error': 'Permission scope denied. Requires scopes: ' + ', '.join(self.scopes)}
