from urllib.parse import urlparse, parse_qs

from .session import APISession
from .client import LogAPI, AssetAPI, TermAPI, AreaAPI

class farmOS:

    """Create a new farmOS instance.

    Keyword Arguments:
    hostname - the farmOS hostname (without protocol)
    username - the farmOS username
    password - the farmOS user's password

    Attributes:
    session - an APISession object that handles HTTP requests

    """

    def __init__(self, hostname, username, password):
        self.session = APISession(hostname, username, password)
        self.log = LogAPI(self.session)
        self.asset = AssetAPI(self.session)
        self.area = AreaAPI(self.session)
        self.term = TermAPI(self.session)


    def authenticate(self):
        """Authenticates with the farmOS site.

        Returns True or False indicating whether or not
        the authentication was successful
        """
        return self.session.authenticate()

    def info(self):
        """Retrieve info about the farmOS instance"""
        response = self.session.http_request(path='farm.json')
        if (response.status_code == 200):
            return response.json()

        return []

    def vocabulary(self, machine_name=None):
        path='taxonomy_vocabulary.json'
        params = {}
        params['machine_name'] = machine_name

        response = self.session.http_request(path=path, params=params)

        if (response.status_code == 200):
            data = response.json()
            if 'list' in data:
                return data['list']

        return []
