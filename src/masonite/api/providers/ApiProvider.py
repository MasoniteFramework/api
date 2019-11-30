''' A ScheduleProvider Service Provider '''
from masonite.provider import ServiceProvider
from ..guards import APIGuard
from masonite.auth import Auth


class ApiProvider(ServiceProvider):

    wsgi = False

    def register(self):
        pass

    def boot(self, auth: Auth):
        auth.register_guard('api', APIGuard)
