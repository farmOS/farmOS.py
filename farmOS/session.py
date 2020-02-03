import logging

from requests import Session
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

from .exceptions import NotAuthenticatedError

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

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

    def __init__(self, hostname,
                 grant_type,
                 client_id,
                 client_secret=None,
                 scope=None,
                 username=None,
                 password=None,
                 token=None,
                 redirect_uri=None,
                 token_url=None,
                 authorization_url=None,
                 token_updater=None,
                 *args, **kwargs):

        # Initialize the session as not authenticated.
        self.authenticated = False
        self.csrf_token = None

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
                                               token_updater=token_updater,
                                               scope=scope)
        elif grant_type == "Password":
            super(OAuthSession, self).__init__(token=token,
                                               client=LegacyApplicationClient(client_id=client_id),
                                               auto_refresh_url=token_url,
                                               auto_refresh_kwargs=auto_refresh_kwargs,
                                               token_updater=token_updater,
                                               scope=scope)

        # Check if 'user_access' scope is included.
        # If so, indicate that we have full User Access and should request
        # a CSRF token to allow making non-GET requests.
        self.has_user_access = scope.find('user_access') > -1

        # Save values for later use.
        self._token_url = token_url
        self._authorization_base_url = authorization_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._username = username
        self._password = password
        self.hostname = hostname

    def authenticate(self):
        """Authenticates with the farmOS site.

        Returns True or False indicating whether or not
        the authentication was successful
        """
        token = self.token

        if 'access_token' not in token:
            logger.debug('Retrieving new OAuth Token.')

            if self.grant_type == "Authorization":
                authorization_url, state = self.authorization_url(self._authorization_base_url,
                                                                  access_type="offline",
                                                                  prompt="select_account")

                print('Please go here and authorize,', authorization_url)

                # Get the authorization verifier code from the callback url
                redirect_response = input('Paste the full redirect URL here:')

                # Fetch the access token
                token = self.fetch_token(self._token_url,
                                         client_secret=self._client_secret,
                                         authorization_response=redirect_response)

            elif self.grant_type == "Password":
                token = self.fetch_token(token_url=self._token_url,
                                         client_id=self._client_id,
                                         client_secret=self._client_secret,
                                         username=self._username,
                                         password=self._password,
                                         scope=self.scope)

            logger.debug('Fetched OAuth Access Token %s', token)

            # Save the token.
            logger.debug('Saving token with token_updater utility.')
            self.token_updater(token)

        # If the OAuth Token has user access, request a session token
        # from the RESTful Web Services module. This is required for
        # non HTTP GET requests.
        if self.has_user_access:
            self.csrf_token = _get_csrf_token(self)

        return self.is_authenticated(check=True)

    def http_request(self, path, method='GET', options=None, params=None, force=False):
        """Raw HTTP request helper function.

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

        headers = {}
        # Automatically add the token to the request, if it exists.
        # Give precedence to a token passed in with options['headers']['X-CSRF-Token'].
        if options and 'headers' in options and 'X-CSRF-Token' in options['headers']:
            headers['X-CSRF-Token'] = options['headers']['X-CSRF-Token']
        if self.csrf_token is not None:
            headers['X-CSRF-Token'] = self.csrf_token

        # Return response from the _http_request helper function.
        return _http_request(self, path, method, options, params, headers)

    def is_authenticated(self, check=False):
        """Helper function that returns True or False if the Session is Authenticated"""
        # If the OAuth Token has user access, check if the session
        # has a csrf_token. This is required for non HTTP GET requests.
        if self.has_user_access and self.csrf_token is None:
            return False

        if check is False:
            return self.authenticated
        else:
            return _is_authenticated(self)


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
        super(DrupalAuthSession, self).__init__()

        # Initialize the session as not authenticated.
        self.authenticated = False

        # Store farmOS authentication credentials
        self.hostname = hostname
        self.username = username
        self.password = password

        # Store the authentication token
        self.csrf_token = None

    def authenticate(self):
        """Authenticates with the farmOS site.

        Returns True or False indicating whether or not
        the authentication was successful
        """
        logger.debug('Authenticating with Drupal Login Form')
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
        self.csrf_token = _get_csrf_token(self)

        return self.is_authenticated(check=True)

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
        if self.csrf_token:
            headers['X-CSRF-Token'] = self.csrf_token

        # Return response from the _http_request helper function.
        return _http_request(self, path, method, options, params, headers)

    def is_authenticated(self, check=False):
        """Helper function that returns True or False if the Session is Authenticated"""
        # Check if the session has a csrf_token
        if self.csrf_token is None:
            return False

        if check is False:
            return self.authenticated
        else:
            return _is_authenticated(self)


def _http_request(session, path, method='GET', options=None, params=None, headers=None):
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

    if headers is None:
        headers = {}

    # Perform the request.
    response = session.request(method,
                               url,
                               headers=headers,
                               allow_redirects=allow_redirects,
                               data=data,
                               json=json,
                               params=params)

    # If this is a POST request, and a redirect occurred, attempt to re-POST.
    redirect_codes = [300, 301, 302, 303, 304, 305, 306, 307, 308]
    if method in ['POST', 'PUT'] and response.status_code in redirect_codes:
        if response.headers['Location']:
            response = session.request(method,
                                       response.headers['Location'],
                                       headers=headers,
                                       allow_redirects=True,
                                       data=data,
                                       json=json, params=params)

    # Return the response.
    return response

def _get_csrf_token(session):
    """Helper function to retrieve a CSRF Session Token"""
    csrf_token = None

    logger.debug('Retrieving new csrf_token.')

    # Request a session token from the RESTful Web Services module
    response = session.http_request('restws/session/token', force=True)
    if response:
        if response.status_code == 200:
            csrf_token = response.text

    return csrf_token


def _is_authenticated(session):
    """Helper function to check if the Session is authenticated."""

    try:
        response = session.http_request(path='farm.json', force=True)
    except NotAuthenticatedError:
        return False

    if response.status_code == 200:
        session.authenticated = True
        return True
    else:
        session.authenticated = False
        return False
