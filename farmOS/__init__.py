from datetime import datetime
from urllib.parse import urlparse, urlunparse

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

    def __init__(self, hostname=None, username=None, password=None, client_id=None, client_secret=None, config_file=None,
                 profile_name=None, token_updater=None):
        # Start a list of config files.
        config_file_list = ['farmos_default_config.cfg']

        # Append additional config files.
        self.config_file = None
        if config_file is not None:
            if isinstance(config_file, str):
                config_file_list.append(config_file)
                self.config_file = config_file
            else:
                raise Exception("Config file must be a string.")

        # Create a ClientConfig object.
        self.config = ClientConfig()
        # Read config files.
        self.config.read(config_file_list)

        # Use a profile if provided.
        self.profile = None
        self.profile_name = "DEFAULT"
        if profile_name is not None:
            self.use_profile(profile_name, create_profile=True)

        # Load the config boolean for development mode.
        self.development = self.config.getboolean(self.profile_name, "development", fallback=False)

        # Allow authentication over HTTP in development mode
        # or if the oauth_insecure_transport config is enabled.
        oauth_insecure_transport = self.config.getboolean(self.profile_name, "oauthlib_insecure_transport", fallback=False)
        if self.development or oauth_insecure_transport:
            import os
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        self.session = None

        # A username or client_id is required for authentication to farmOS.
        if username is None and client_id is None:
            # Try to load values from config profile.
            if self.has_profile():
                hostname = self.config.get(self.profile_name, "hostname", fallback=None)
                username = self.config.get(self.profile_name, "username", fallback=None)
                password = self.config.get(self.profile_name, "password", fallback=None)
                client_id = self.config.get(self.profile_name, "client_id", fallback=None)
                client_secret = self.config.get(self.profile_name, "client_secret", fallback=None)

            # Check if required values were populated.
            if username is None and client_id is None:
                raise Exception("No authentication method provided.")

        if hostname is not None:
            valid_schemes = ["http", "https"]
            default_scheme = "http" if self.development else "https"
            parsed_url = urlparse(hostname)

            # Validate the hostname.
            # Add a default scheme if not provided.
            if not parsed_url.scheme:
                parsed_url = parsed_url._replace(scheme=default_scheme)

            # Check for a valid scheme.
            if parsed_url.scheme not in valid_schemes:
                raise Exception("Not a valid scheme.")

            # If not netloc was provided, it was probably parsed as the path.
            if not parsed_url.netloc and parsed_url.path:
                parsed_url = parsed_url._replace(netloc=parsed_url.path)
                parsed_url = parsed_url._replace(path='')

            # Check for netloc.
            if not parsed_url.netloc:
                raise Exception("Invalid hostname. Must have netloc.")

            # Don't allow path, params, or query.
            if parsed_url.path or parsed_url.params or parsed_url.query:
                raise Exception("Hostname cannot include path and query parameters.")

            # Build the url again to include changes.
            hostname = urlunparse(parsed_url)

            # Save the hostname in the config.
            self.config.set(self.profile_name, "hostname", hostname)

        else:
            raise Exception("No hostname provided and could not be loaded from config.")

        # Ask for password if username is given without a password.
        if username is not None and password is None:
            from getpass import getpass
            password = getpass('Enter password: ')

        # Default to simple token_saver to save tokens to config.
        if token_updater is None:
            token_updater = self.save_token

        # If a client_id is supplied, try to create an OAuth Session
        if client_id is not None:
            token_url = self.config.get(self.profile_name, "oauth_token_url")

            # Load saved Authentication Profile from config.
            token = None
            if self.has_profile():
                # Save OAuth Client ID to config.
                self.config.set(self.profile_name, "client_id", client_id)
                self.config.set(self.profile_name, "client_secret", client_secret)

                token = dict(self.profile)

                # If an access_token is not saved, do not use the token dict.
                if 'access_token' not in token:
                    token = {}

                # Unset the expires_in key.
                token.pop('expires_in', None)

                # Check the token expiration time.
                if 'expires_at' in token:
                    # Create datetime objects for comparison.
                    now = datetime.now()
                    expiration_time = datetime.fromtimestamp(float(token['expires_at']))

                    # Calculate seconds until expiration.
                    timedelta = expiration_time - now
                    expires_in = timedelta.total_seconds()

                    # Update the token expires_in value
                    token['expires_in'] = expires_in

                # Unset the expires_at key.
                token.pop('expires_at', None)

            # Create an OAuth Session with the Password Credentials Grant.
            if username is not None and password is not None:
                self.config.set(self.profile_name, "username", username)
                self.config.set(self.profile_name, "password", password)
                self.session = OAuthSession(grant_type="Password",
                                            hostname=hostname,
                                            client_id=client_id,
                                            client_secret=client_secret,
                                            username=username,
                                            password=password,
                                            token=token,
                                            token_url=token_url,
                                            token_updater=token_updater)

            # Create an OAuth Session with the Authorization Code Grant.
            else:
                # Load saved OAuth URLs from config.
                authorization_url = self.config.get(self.profile_name, "oauth_authorization_url")
                redirect_url = self.config.get(self.profile_name, "oauth_redirect_url")

                # Create an OAuth Session
                self.session = OAuthSession(grant_type="Authorization",
                                            hostname=hostname,
                                            client_id=client_id,
                                            client_secret=client_secret,
                                            token=token,
                                            redirect_uri=redirect_url,
                                            token_url=token_url,
                                            authorization_url=authorization_url,
                                            token_updater=token_updater)

        # Fallback to DrupalAPISession
        if client_id is None and username is not None and password is not None:
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

        # Authenticate the session if auto_authenticate is enabled
        # and the session has not already been authenticated.
        # (OAuthSession will authenticate if an existing token was provided at startup)
        auto_authenticate = self.config.getboolean(self.profile_name, "auto_authenticate", fallback=True)
        if auto_authenticate and not self.session.is_authenticated():
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
        # Only save values if a profile name was defined.
        if self.has_profile():
            profile_name = self.get_profile_name()
            if 'access_token' in token:
                self.config.set(profile_name, "access_token", token['access_token'])

            if 'expires_in' in token:
                # token['expires_in'] is an int, the access_token lifetime.
                # Must be saved as a string in the config.
                self.config.set(profile_name, "expires_in", str(token['expires_in']))

            if 'token_type' in token:
                self.config.set(profile_name, "token_type", token['token_type'])

            if 'refresh_token' in token:
                self.config.set(profile_name, "refresh_token", token['refresh_token'])

            if 'expires_at' in token:
                # token['expires_at'] is a float, the access_token expiration time.
                # requests-oauthlib generates this value as
                #       expires_at = time.time() + expires_in
                # Must be saved as a string in the config.
                self.config.set(profile_name, "expires_at", str(token['expires_at']))

        if self.config_file is not None:
            self.config.write(path=self.config_file)

    def create_profile(self, profile_name):
        """Creates a Section for profile_name in farm.config."""
        if not self._profile_exists(profile_name):
            self.config.add_section(profile_name)
            return True
        else:
            # TODO: Write test for duplicate profile names.
            raise Exception("Profile '" + profile_name + "' already exists.")

    def has_profile(self, profile_name=None):
        """Returns True or False if the client is configured with a profile.

        Also returns whether a profile_name is found in the config.
        """
        if profile_name is not None:
            return self._profile_exists(profile_name)
        else:
            return self.profile is not None

    def get_profile_name(self):
        """Returns the current profile name."""
        if self.has_profile():
            return self.profile_name
        else:
            raise Exception("No profile being used.")

    def use_profile(self, profile_name, create_profile=False):
        """Set the authentication profile to use from farm.config."""
        profile = self._get_profile_config(profile_name)

        if profile is None:
            if create_profile is True:
                self.create_profile(profile_name)
                profile = self._get_profile_config(profile_name)
            else:
                # TODO: Write test for no profile name.
                raise Exception("Profile '" + profile_name + "' does not exist.")

        self.profile = profile
        self.profile_name = profile_name

    def _get_profile_config(self, profile_name=None):
        """Helper function that returns the current profile config, or the config or profile_name."""
        if self._profile_exists(profile_name):
            return self.config[profile_name]
        else:
            return None

    def _profile_exists(self, profile_name):
        """Helper function to check if a profile for profile_name exists."""
        if isinstance(profile_name, str):
            return self.config.has_section(profile_name)
        else:
            # TODO: Write test for invalid profile_name.
            raise Exception("profile_name not a String.")
