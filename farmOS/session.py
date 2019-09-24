from requests import Session
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

from .exceptions import NotAuthenticatedError

class OAuthSession(OAuth2Session):
    """OAuthSession uses OAuth2 to authenticate with farmOS

    This class stores access tokens and refresh tokens used to
    authenticate with the farmOS server for all requests.

    Keyword Arguments:
        hostname - the farmOS hostname (without protocol)
        client_id - the farmOS API Client ID
        client_secret - the farmOS API Client Secret
        username - the farmOS username (for OAuth2 Password Grant)
        password - the farmOS user's password (for OAuth2 Password Grant)
    """

    def __init__(self, hostname, client_id, grant_type, client_secret=None, username=None, password=None, token=None,
                 redirect_uri=None, token_url=None, authorization_url=None, token_updater = None, *args, **kwargs):
        # Initialize the session as not authenticated.
        self.authenticated = False

        # Provide a default token_saver is nothing is provided.
        self.token_updater = self._token_saver
        # Save a provided token updater.
        if token_updater is not None:
            self.token_updater = token_updater

        # Create a dictionary of credentials required to pass along with Refresh Tokens
        # Required to generate a new access token
        auto_refresh_kwargs = {'client_id': client_id,
                               'client_secret': client_secret
                               }

        # Validate the grant type.
        valid_grant_types = ["Authorization", "Password"]
        if grant_type not in valid_grant_types:
            raise Exception(grant_type + " is not a supported OAuth Grant Type")

        # Save the Grant Type
        self.grant_type = grant_type

        if grant_type == "Authorization":
            super(OAuthSession, self).__init__(token=token,
                                               client_id=client_id,
                                               redirect_uri=redirect_uri,
                                               auto_refresh_url=token_url,
                                               auto_refresh_kwargs=auto_refresh_kwargs,
                                               token_updater=self.token_updater)
        elif grant_type == "Password":
            super(OAuthSession, self).__init__(token=token,
                                               client=LegacyApplicationClient(client_id=client_id),
                                               auto_refresh_url=token_url,
                                               auto_refresh_kwargs=auto_refresh_kwargs,
                                               token_updater=self.token_updater)

        # Save values for later use.
        self._token_url = token_url
        self._authorization_base_url = authorization_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._username = username
        self._password = password
        self.hostname = hostname

        # Check if an existing token was provided.
        if token is not None and 'access_token' in token:
            self.is_authenticated(check=True)

    def authenticate(self):
        """Authenticates with the farmOS site.

        Returns True or False indicating whether or not
        the authentication was successful
        """
        if self.grant_type == "Authorization":
            authorization_url, state = self.authorization_url(self._authorization_base_url,
                                                                access_type="offline", prompt="select_account")

            print('Please go here and authorize,', authorization_url)

            # Get the authorization verifier code from the callback url
            redirect_response = input('Paste the full redirect URL here:')

            # Fetch the access token
            token = self.fetch_token(self._token_url, client_secret=self._client_secret, authorization_response=redirect_response)
        elif self.grant_type == "Password":
            token = self.fetch_token(token_url=self._token_url,
                                     client_id=self._client_id,
                                     client_secret=self._client_secret,
                                     username=self._username,
                                     password=self._password)

        # Save the token.
        self.token_updater(token)

        return self.is_authenticated(check=True)

    def http_request(self, path, method='GET', options=None, params=None, force=False):
        """Raw HTTP request helper function.

        Keyword arguments:
        :param path: the URL path.
        :param method: the HTTP method.
        :param options: a dictionary of data and parameters to pass on to the request.
        :param params: URL query parameters.
        :return: requests response object.
        """

        # If the session has not been authenticated
        # and the request does not have force=True,
        # raise NotAuthenticatedError
        if not self.is_authenticated() and not force:
            raise NotAuthenticatedError()

        # Return response from the _http_request helper function.
        return _http_request(self, path, method, options, params)

    def is_authenticated(self, check=False):
        """Helper function that returns True or False if the Session is Authenticated"""
        if check is False:
            return self.authenticated
        else:
            return _is_authenticated(self)

    def _token_saver(self, token):
        """A utility to save tokens in the OAuth Session

        Saves Authentication and Refresh Tokens within the session.

        :param token: The OAuth2 token dictionary.
        """
        print("Got a new token: " + token['access_token'] + " expires in " + token['expires_in'])
        self.token = token

# Use a Requests Session to store cookies across requests.
#   http://docs.python-requests.org/en/master/user/advanced/#session-objects
class DrupalAuthSession(Session):

    """APISession handles all HTTP requests for the farmOS API

    This class stores cookies and tokens required for the Drupal
    RESTFul Web Services HTTP Session Authentication method.
    These values are use in all requests made to the farmOS host.

    Keyword Arguments:
    hostname - the farmOS hostname (without protocol)
    username - the farmOS username
    password - the farmOS user's password
    """

    def __init__(self, hostname, username, password, *args, **kwargs):
        super(DrupalAuthSession, self).__init__(*args, **kwargs)

        # Initialize the session as not authenticated.
        self.authenticated = False

        # Store farmOS authentication credentials
        self.hostname = hostname
        self.username = username
        self.password = password

        # Store the authentication token
        self.token = ''

    def authenticate(self):
        """Authenticates with the farmOS site.

        Returns True or False indicating whether or not
        the authentication was successful
        """

        # Clear any previously populated token.
        self.token = ''

        # Prepare the data payload
        options = {
            'data': {
                'name': self.username,
                'pass': self.password,
                'form_id': 'user_login',
            }
        }

        # Login with the username and password to get a cookie.
        response = self.http_request('user/login', 'POST', options, force=True)
        if response:
            if response.status_code != 200:
                return False

        # Request a session token from the RESTful Web Services module
        response = self.http_request('restws/session/token', force=True)
        if response:
            if response.status_code == 200:
                self.token = response.text

        # Return True if the token was populated.
        if self.token:
            return self.is_authenticated(check=True)
        else:
            return False

    def http_request(self, path, method='GET', options=None, params=None, force=False):
        """Make an HTTP request.

        Keyword arguments:
        :param path: the URL path.
        :param method: the HTTP method.
        :param options: a dictionary of data and parameters to pass on to the request.
        :param params: URL query parameters.
        :param force: Force the request regardless of Authenticated status.
        :return: requests response object.
        """

        # If the session has not been authenticated
        # and the request does not have force=True,
        # raise NotAuthenticatedError
        if not self.is_authenticated() and not force:
            raise NotAuthenticatedError()

        # Start a headers dictionary.
        headers = {}

        # Automatically add the token to the request, if it exists.
        # Give precedence to a token passed in with options['headers']['X-CSRF-Token'].
        if options and 'headers' in options and 'X-CSRF-Token' in options['headers']:
            headers['X-CSRF-Token'] = options['headers']['X-CSRF-Token']
        if self.token:
            headers['X-CSRF-Token'] = self.token

        # Return response from the _http_request helper function.
        return _http_request(self, path, method, options, params, headers)

    def is_authenticated(self, check=False):
        """Helper function that returns True or False if the Session is Authenticated"""
        if check is False:
            return self.authenticated
        else:
            return _is_authenticated(self)

def _http_request(session, path, method='GET', options=None, params=None, headers={}):
    """Raw HTTP request helper function.

    Keyword arguments:
    :param session: The requests Session object to call a request with.
    :param path: the URL path.
    :param method: the HTTP method.
    :param options: a dictionary of data and parameters to pass on to the request.
    :param params: URL query parameters.
    :param headers: Dictionary of HTTP headers to include in the request.
    :return: requests response object.

    """
    # Strip protocol, hostname, leading/trailing slashes, and whitespace from the path.
    path = path.strip('/')
    path = path.strip()

    # Assemble the URL.
    url = '{}/{}'.format(session.hostname, path)

    # Automatically follow redirects, unless this is a POST request.
    # The Python requests library converts POST to GET during a redirect.
    # Allow this to be overridden in options.
    allow_redirects = True
    if method in ['POST', 'PUT']:
        allow_redirects = False
    if options and 'allow_redirects' in options:
        allow_redirects = options['allow_redirects']

    # If there is data to be sent, include it.
    data = None
    if options and 'data' in options:
        data = options['data']

    # If there is a json data to be sent, include it.
    json = None
    if options and 'json' in options:
        json = options['json']

    # Perform the request.
    response = session.request(method, url, headers=headers, allow_redirects=allow_redirects, data=data, json=json,
                            params=params)

    # If this is a POST request, and a redirect occurred, attempt to re-POST.
    redirect_codes = [300, 301, 302, 303, 304, 305, 306, 307, 308]
    if method in ['POST', 'PUT'] and response.status_code in redirect_codes:
        if response.headers['Location']:
            response = session.request(method, response.headers['Location'], headers=headers, allow_redirects=True, data=data,
                                    json=json, params=params)

    # Return the response.
    return response

def _is_authenticated(session):
    """Helper function to check if the Session is authenticated."""

    try:
        response = session.http_request(path='farm.json', force=True)
    except NotAuthenticatedError:
        return False

    if (response.status_code == 200):
        session.authenticated = True
        return True
    else:
        session.authenticated = False
        return False
