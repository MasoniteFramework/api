""" Database Settings """

import os

from masonite.environment import LoadEnvironment
from orator import DatabaseManager, Model

"""
|--------------------------------------------------------------------------
| Load Environment Variables
|--------------------------------------------------------------------------
|
| Loads in the environment variables when this page is imported.
|
"""

LoadEnvironment()

"""
|--------------------------------------------------------------------------
| Database Settings
|--------------------------------------------------------------------------
|
| Set connection database settings here as a dictionary. Follow the
| format below to create additional connection settings.
|
| @see Orator migrations documentation for more info
|
"""

DATABASES = {
    'default': 'sqlite',
    'sqlite': {
        'driver': 'sqlite',
        'database': 'package.db'
    },
}

DB = DatabaseManager(DATABASES)
Model.set_connection_resolver(DB)
