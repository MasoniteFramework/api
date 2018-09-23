from api.exceptions import PermissionScopeDenied

class PermissionScopes:

    scopes = ['*']
    
    def scopes(self, scopes: list):
        raise PermissionScopeDenied

    def run_scopes(self, scopes: list):
        try:
            return self.scopes(scopes)
        except PermissionScopeDenied:
            return {'error': 'permission scope denied'}