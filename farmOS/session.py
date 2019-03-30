import requests

from .exceptions import NotAuthenticatedError

# Use a Requests Session to store cookies across requests.
#   http://docs.python-requests.org/en/master/user/advanced/#session-objects
class APISession(requests.Session):

    """APISession handles all HTTP requests for the farmOS API

    This class stores cookies and tokens generated from authentication
    across all requests made to the farmOS host.

    Keyword Arguments:
    hostname - the farmOS hostname (without protocol)
    username - the farmOS username
    password - the farmOS user's password
    """

    def __init__(self, hostname, username, password, *args, **kwargs):
        super(APISession, self).__init__(*args, **kwargs)

        # Store farmOS authentication credentials
        self.hostname = hostname
        self.username = username
        self.password = password

        # Store the authentication token
        self.token = ''

        self.authenticated = False

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
            self.authenticated = True
            return True
        else:
            return False

    def http_request(self, path, method='GET', options=None, params=None, force=False):
        """Raw HTTP request helper function.

        Keyword arguments:
        path - URL path (without hostname)
        method - the HTTP method
        options - a dictionary of data and parameters to pass on to the request

        """

        # If the session has not been authenticated
        # and the request does not have force=True,
        # raise NotAuthenticatedError
        if not self.authenticated and not force:
            raise NotAuthenticatedError()

        # Strip protocol, hostname, leading/trailing slashes, and whitespace from the path.
        remove = [
            'http://',
            'https://',
            self.hostname,
        ]
        for string in remove:
            path = path.replace(string, '')
        path = path.strip('/')
        path = path.strip()

        # Assemble the URL.
        url = 'http://{}/{}'.format(self.hostname, path)

        # Start a headers dictionary.
        headers = {}

        # Automatically add the token to the request, if it exists.
        # Give precedence to a token passed in with options['headers']['X-CSRF-Token'].
        if options and 'headers' in options and 'X-CSRF-Token' in options['headers']:
            headers['X-CSRF-Token'] = options['headers']['X-CSRF-Token']
        if self.token:
            headers['X-CSRF-Token'] = self.token

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
        response = self.request(method, url, headers=headers, allow_redirects=allow_redirects, data=data, json=json, params=params)

        # If this is a POST request, and a redirect occurred, attempt to re-POST.
        redirect_codes = [300, 301, 302, 303, 304, 305, 306, 307, 308]
        if method in ['POST', 'PUT'] and response.status_code in redirect_codes:
            if response.headers['Location']:
                response = self.request(method, response.headers['Location'], headers=headers, allow_redirects=True, data=data, json=json, params=params)

        # Return the response.
        return response
