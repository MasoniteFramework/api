from api.exceptions import PermissionScopeDenied

class PermissionScopes:

    scopes = ['*']

    def scope(self):
        token = self.get_token()
        if self.scopes == ['*']:
            return

        if 'scopes' not in token or not set(self.scopes).issubset(token['scopes'].split(',')):
            raise PermissionScopeDenied

    def run_scope(self):
        try:
            return self.scope()
        except PermissionScopeDenied:
            return {'error': 'Permission scope denied. Requires scopes: ' + ', '.join(self.scopes)}
