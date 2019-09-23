from .session import DrupalAuthSession, OAuthSession
from .client import LogAPI, AssetAPI, TermAPI, AreaAPI
from .config import ClientConfig

class farmOS:

    """Create a new farmOS instance.

    Keyword Arguments:
    hostname - the farmOS hostname (without protocol)
    username - the farmOS username
    password - the farmOS user's password

    Attributes:
    session - an APISession object that handles HTTP requests

    """

    def __init__(self, hostname, username=None, password=None, client_id=None, client_secret=None, config_files=None):
        # Start a list of config files.
        config_file_list = ['farmos_default_config.cfg']

        # Append additional config files.
        if config_files is not None:
            if isinstance(config_files, list):
                config_file_list.extend(config_files)
            elif isinstance(config_files, str):
                config_file_list.append(config_files)
            else:
                print("config_files must be List or String.")

        # Create a ClientConfig object.
        self.config = ClientConfig()
        # Read config files.
        self.config.read(config_file_list)

        self.session = None

        # TODO: validate the hostname
        #   validate the url with urllib.parse

        # A username or client_id is required for authentication to farmOS.
        if username is None and client_id is None:
            raise Exception("No authentication method provided.")

        # Ask for password if username is given without a password.
        if username is not None and password is None:
            from getpass import getpass
            password = getpass('Enter password: ')

        # If a client_id is supplied, try to create an OAuth Session
        if client_id is not None:
            redirect_uri = self.config.get("oauth", "oauth_redirect_uri")
            token_url = self.config.get("oauth", "oauth_token_url")
            self.session = OAuthSession(hostname=hostname, client_id=client_id, client_secret=client_secret,
                                        redirect_uri=redirect_uri, token_url=token_url)

        # Fallback to DrupalAPISession
        if username is not None and password is not None:
            # Create a session with requests
            self.session = DrupalAuthSession(hostname, username, password)

        self._username = username
        self._client_id = client_id
        self._client_secret = client_secret

        if self.session is None:
            raise Exception("Could not create a session object. Supply authentication credentials when "\
                            "initializing a farmOS Client.")

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
