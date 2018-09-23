from api.exceptions import PermissionScopeDenied

class PermissionScopes:

    scopes = ['*']
    
    def scopes(self, scopes: list):
        raise PermissionScopeDenied

    def run_scopes(self):
        try:
            return self.scopes()
        except PermissionScopeDenied:
            return {'error': 'permission scope denied'}