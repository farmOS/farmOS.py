import requests


class farmOS:

    # Store authentication credentials.
    hostname = ''
    username = ''
    password = ''

    # Store cookie jar and authentication token internally.
    jar = requests.cookies.RequestsCookieJar()

    # Store authentication token internally.
    token = ''

    def __init__(self, hostname, username, password):
        """Create a new farmOS instance."""
        self.hostname = hostname
        self.username = username
        self.password = password

    def authenticate(self):
        """Authenticate with the farmOS site."""

        # If any of the authentication credentials are empty, bail.
        if not self.hostname or not self.username or not self.password:
            print('farmOS authentication failed: missing hostname, username, or password.')
            return

        # Create a cookie jar to store the session cookie.
        self.jar = requests.cookies.RequestsCookieJar()

        # Clear any previously populated token.
        self.token = ''

        # Login with the username and password to get a cookie.
        options = {
            'data': {
                'name': self.username,
                'pass': self.password,
                'form_id': 'user_login',
            }
        }
        response = self.httpRequest('user/login', 'POST', options)
        if response:
            if response.status_code != 200:
                return False

        # Request a session token from the RESTful Web Services module
        response = self.httpRequest('restws/session/token')
        if response:
            if response.status_code == 200:
                self.token = response.text

        # Return True if the token was populated.
        if self.token:
            return True
        else:
            return False

    def httpRequest(self, path, method='GET', options=None):
        """Raw HTTP request helper function."""

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

        # Add configuration to use strict RFC compliant redirects (so that POST data is forwarded to the new
        # destination). This allows for HTTP to be redirected to HTTPS automatically.
        # Allow this to be overridden in options.
        allow_redirects = True
        if options and 'allow_redirects' in options:
            allow_redirects = options['allow_redirects']

        # If there is data to be sent, include it.
        data = None
        if options and 'data' in options:
            data = options['data']

        # Perform the request and return the response
        return requests.request(method, url, cookies=self.jar, headers=headers, allow_redirects=allow_redirects, data=data)
