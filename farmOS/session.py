import requests

# Use a Requests Session to store cookies across requests.
#   http://docs.python-requests.org/en/master/user/advanced/#session-objects
class APISession(requests.Session):
    def __init__(self, hostname, username, password, *args, **kwargs):
        super(APISession, self).__init__(*args, **kwargs)

        # Store farmOS authentication credentials
        self.hostname = hostname
        self.username = username
        self.password = password

        # Store the authentication token
        self.token = ''

    def authenticate(self):
        """Authenticate with the farmOS site."""

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
        response = self.http_request('user/login', 'POST', options)
        if response:
            if response.status_code != 200:
                return False

        # Request a session token from the RESTful Web Services module
        response = self.http_request('restws/session/token')
        if response:
            if response.status_code == 200:
                self.token = response.text

        # Return True if the token was populated.
        if self.token:
            return True
        else:
            return False

    def http_request(self, path, method='GET', options=None, params=None):
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

        # Automatically follow redirects, unless this is a POST request.
        # The Python requests library converts POST to GET during a redirect.
        # Allow this to be overridden in options.
        allow_redirects = True
        if method == 'POST':
            allow_redirects = False
        if options and 'allow_redirects' in options:
            allow_redirects = options['allow_redirects']

        # If there is data to be sent, include it.
        data = None
        if options and 'data' in options:
            data = options['data']

        # Perform the request.
        response = self.request(method, url, headers=headers, allow_redirects=allow_redirects, data=data, params=params)

        # If this is a POST request, and a redirect occurred, attempt to re-POST.
        redirect_codes = [300, 301, 302, 303, 304, 305, 306, 307, 308]
        if method == 'POST' and response.status_code in redirect_codes:
            if response.headers['Location']:
                response = self.request(method, response.headers['Location'], headers=headers, allow_redirects=True, data=data, params=params)

        # Return the response.
        return response
