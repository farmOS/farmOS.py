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

        # Load the config boolean for development mode.
        self.development = self.config.getboolean("Client", "development", fallback=False)

        # Allow authentication over HTTP in development mode
        # or if the oauth_insecure_transport config is enabled.
        oauth_insecure_transport = self.config.getboolean("OAuth", "oauthlib_insecure_transport", fallback=False)
        if self.development or oauth_insecure_transport:
            import os
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        self.session = None

        # TODO: validate the hostname
        #   validate the url with urllib.parse
        # Save the hostname in the authentication configuration.
        self.config.set("Authentication", "hostname", hostname)

        # A username or client_id is required for authentication to farmOS.
        if username is None and client_id is None:
            raise Exception("No authentication method provided.")

        # Ask for password if username is given without a password.
        if username is not None and password is None:
            from getpass import getpass
            password = getpass('Enter password: ')

        # If a client_id is supplied, try to create an OAuth Session
        if client_id is not None:
            redirect_url = self.config.get("OAuth", "oauth_redirect_url")
            token_url = self.config.get("OAuth", "oauth_token_url")
            authorization_url = self.config.get("OAuth", "oauth_authorization_url")
            self.session = OAuthSession(hostname=hostname, client_id=client_id, client_secret=client_secret,
                                        token=token, redirect_uri=redirect_url, token_url=token_url,
                                        authorization_url=authorization_url, token_updater=self.save_token)

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

        if self.config.getboolean("Client", "auto_authenticate"):
            self.session.authenticate()

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

    def save_token(self, token):
        """Save an OAuth Token to config for later use.

        This method accepts an OAuth token and saves values to the Authentication
        section of the farm.config ClientConfig object. It is primarily used as
        a callback for the requests-oauthlib OAuth2Session automatic token refreshing
        functionality. But this method could be used by others to supply a farmOS client
        with existing OAuth tokens to use (and persist).

        :param token: OAuth token dict.
        :return: None.
        """
        if 'access_token' in token:
            self.config.set("Authentication", "access_token", token['access_token'])

        if 'expires_in' in token:
            self.config.set("Authentication", "expires_in", token['expires_in'])

        if 'token_type' in token:
            self.config.set("Authentication", "token_type", token['token_type'])

        if 'refresh_token' in token:
            self.config.set("Authentication", "refresh_token", token['refresh_token'])

        if 'expires_at' in token:
            # Save the 'expires_in' as a string. configparser only accepts strings, the
            # requests-oauthlib module does not save this value as a string. Bug?
            self.config.set("Authentication", "expires_at", str(token['expires_at']))

        # TODO: Save the first token values retrieved from
        #  a successful OAuth Authorization Code Grant

        # TODO: rewrite the token values to config on every change.
