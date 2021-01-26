import logging

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class OAuthSession(OAuth2Session):
    """OAuthSession uses OAuth2 to authenticate with farmOS"""

    def __init__(
        self,
        hostname,
        client_id,
        client_secret=None,
        scope=None,
        token=None,
        token_url=None,
        authorization_url=None,
        token_updater=None,
        *args,
        **kwargs
    ):

        # Default to the "user_access" scope.
        if scope is None:
            scope = "user_access"

        # Create a dictionary of credentials required to pass along with Refresh Tokens
        # Required to generate a new access token
        auto_refresh_kwargs = {"client_id": client_id, "client_secret": client_secret}

        super(OAuthSession, self).__init__(
            token=token,
            client=LegacyApplicationClient(client_id=client_id),
            auto_refresh_url=token_url,
            auto_refresh_kwargs=auto_refresh_kwargs,
            token_updater=token_updater,
            scope=scope,
        )

        # Save values for later use.
        self._token_url = token_url
        self._authorization_base_url = authorization_url
        self._client_id = client_id
        self._client_secret = client_secret
        self.hostname = hostname

    def authorize(self, username, password, scope=None):
        """Authorize with the farmOS OAuth server."""

        token = self.token

        logger.debug("Retrieving new OAuth Token.")

        # Ask for username if not provided.
        if username is None:
            from getpass import getpass

            username = getpass("Enter username: ")

        # Ask for password if not provided.
        if password is None:
            from getpass import getpass

            password = getpass("Enter password: ")

        # Use default scope if none provided.
        if scope is None:
            scope = self.scope

        token = self.fetch_token(
            token_url=self._token_url,
            client_id=self._client_id,
            client_secret=self._client_secret,
            username=username,
            password=password,
            scope=scope,
        )

        logger.debug("Fetched OAuth Access Token %s", token)

        # Save the token.
        logger.debug("Saving token with token_updater utility.")
        if self.token_updater is not None:
            self.token_updater(token)

        return token

    def http_request(self, path, method="GET", options=None, params=None, headers=None):
        """Raw HTTP request helper function.

        Keyword arguments:
        :param path: the URL path.
        :param method: the HTTP method.
        :param options: a dictionary of data and parameters to pass on to the request.
        :param params: URL query parameters.
        :return: requests response object.
        """

        # Strip protocol, hostname, leading/trailing slashes, and whitespace from the path.
        path = path.strip("/")
        path = path.strip()

        # Assemble the URL.
        url = "{}/{}".format(self.hostname, path)
        return self._http_request(
            url=url, method=method, options=options, params=params, headers=headers
        )

    def _http_request(self, url, method="GET", options=None, params=None, headers=None):

        # Automatically follow redirects, unless this is a POST request.
        # The Python requests library converts POST to GET during a redirect.
        # Allow this to be overridden in options.
        allow_redirects = True
        if method in ["POST", "PUT"]:
            allow_redirects = False
        if options and "allow_redirects" in options:
            allow_redirects = options["allow_redirects"]

        if headers is None:
            headers = {}

        # If there is data to be sent, include it.
        data = None
        if options and "data" in options:
            data = options["data"]
            headers["Content-Type"] = "application/vnd.api+json"

        # If there is a json data to be sent, include it.
        json = None
        if options and "json" in options:
            json = options["json"]
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/vnd.api+json"

        # Perform the request.
        response = self.request(
            method,
            url,
            headers=headers,
            allow_redirects=allow_redirects,
            data=data,
            json=json,
            params=params,
        )

        # If this is a POST request, and a redirect occurred, attempt to re-POST.
        redirect_codes = [300, 301, 302, 303, 304, 305, 306, 307, 308]
        if method in ["POST", "PUT"] and response.status_code in redirect_codes:
            if response.headers["Location"]:
                response = self.request(
                    method,
                    response.headers["Location"],
                    allow_redirects=True,
                    data=data,
                    json=json,
                    params=params,
                )

        # Raise exception if error.
        response.raise_for_status()

        # Return the response.
        return response
