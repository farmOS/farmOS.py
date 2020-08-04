import logging

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
                 client_id,
                 client_secret=None,
                 scope=None,
                 token=None,
                 token_url=None,
                 authorization_url=None,
                 token_updater=None,
                 *args, **kwargs):

        # Default to the "user_access" scope.
        if scope is None:
            scope = 'user_access'

        # Create a dictionary of credentials required to pass along with Refresh Tokens
        # Required to generate a new access token
        auto_refresh_kwargs = {'client_id': client_id,
                               'client_secret': client_secret
                               }

        super(OAuthSession, self).__init__(token=token,
                                           client=LegacyApplicationClient(client_id=client_id),
                                           auto_refresh_url=token_url,
                                           auto_refresh_kwargs=auto_refresh_kwargs,
                                           token_updater=token_updater,
                                           scope=scope)

        # Save values for later use.
        self._token_url = token_url
        self._authorization_base_url = authorization_url
        self._client_id = client_id
        self._client_secret = client_secret
        self.hostname = hostname

    def authorize(self, username, password, scope):
        """Authenticates with the farmOS site.

        Returns True or False indicating whether or not
        the authentication was successful
        """
        token = self.token

        logger.debug('Retrieving new OAuth Token.')

        # Ask for username if not provided.
        if username is None:
            from getpass import getpass
            username = getpass('Enter username: ')

        # Ask for password if not provided.
        if password is None:
            from getpass import getpass
            password = getpass('Enter password: ')

        token = self.fetch_token(token_url=self._token_url,
                                 client_id=self._client_id,
                                 client_secret=self._client_secret,
                                 username=username,
                                 password=password,
                                 scope=scope)

        logger.debug('Fetched OAuth Access Token %s', token)

        # Save the token.
        logger.debug('Saving token with token_updater utility.')
        self.token_updater(token)

        return token

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

        # Return response from the _http_request helper function.
        return _http_request(self, path, method, options, params)

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
