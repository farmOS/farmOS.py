import logging
from datetime import datetime
from urllib.parse import urlparse, urlunparse
from functools import partial

from .session import OAuthSession

from . import client
from . import client_2
from . import subrequests

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class farmOS:
    """A client that connects to the farmOS server."""

    def __init__(
        self,
        hostname,
        client_id="farm",
        client_secret=None,
        scope="user_access",
        token=None,
        token_updater=None,
        version="1",
    ):
        """
        Initialize instance of the farmOS client that connects to a single farmOS server.

        :param hostname: Valid hostname without a path or query params. The HTTPS scheme
            will be added if none is specified.
        :param client_id: OAuth Client ID. Defaults to "farm"
        :param client_secret: OAuth Client Secret. Defaults to None.
        :param scope: OAuth Scope. Defaults to "user_access".
        :param token: An existing OAuth token to use.
        :param token_updater: A function used to save OAuth tokens outside of the client.
        """

        logger.debug("Creating farmOS client.")

        # Load the token updater function.
        self.token_updater = None
        if token_updater is not None:
            logger.debug("Using provided token_updater utility.")
            self.token_updater = token_updater

        self.session = None

        if hostname is not None:
            valid_schemes = ["http", "https"]
            default_scheme = "https"
            parsed_url = urlparse(hostname)

            # Validate the hostname.
            # Add a default scheme if not provided.
            if not parsed_url.scheme:
                parsed_url = parsed_url._replace(scheme=default_scheme)
                logger.debug("No scheme provided. Using %s", default_scheme)

            # Check for a valid scheme.
            if parsed_url.scheme not in valid_schemes:
                raise Exception("Not a valid scheme.")

            # If not netloc was provided, it was probably parsed as the path.
            if not parsed_url.netloc and parsed_url.path:
                parsed_url = parsed_url._replace(netloc=parsed_url.path)
                parsed_url = parsed_url._replace(path="")

            # Check for netloc.
            if not parsed_url.netloc:
                raise Exception("Invalid hostname. Must have netloc.")

            # Don't allow path, params, or query.
            if parsed_url.path or parsed_url.params or parsed_url.query:
                raise Exception("Hostname cannot include path and query parameters.")

            # Build the url again to include changes.
            hostname = urlunparse(parsed_url)
            logger.debug("Complete hostname configured as %s", hostname)

        else:
            raise Exception("No hostname provided and could not be loaded from config.")

        logger.debug("Creating an OAuth Session.")
        # OR implement a method to check both token paths.
        # maybe version can default to none, and check the server?
        token_url = hostname + "/oauth/token"

        # Check the token expiration time.
        if token is not None and "expires_at" in token:
            # Create datetime objects for comparison.
            now = datetime.now()
            expiration_time = datetime.fromtimestamp(float(token["expires_at"]))

            # Calculate seconds until expiration.
            timedelta = expiration_time - now
            expires_in = timedelta.total_seconds()

            # Update the token expires_in value
            token["expires_in"] = expires_in

            # Unset the 'expires_at' key.
            token.pop("expires_at")

        # Create an OAuth Session
        self.session = OAuthSession(
            hostname=hostname,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            token=token,
            token_url=token_url,
            token_updater=self.token_updater,
        )

        self._client_id = client_id
        self._client_secret = client_secret

        if self.session is None:
            raise Exception(
                "Could not create a session object. Supply authentication credentials when "
                "initializing a farmOS Client."
            )

        if version == 2:
            self.log = client_2.LogAPI(self.session)
            self.asset = client_2.AssetAPI(self.session)
            self.term = client_2.TermAPI(self.session)
            self.resource = client_2.ResourceBase(self.session)
            self.info = partial(client_2.info, self.session)
            self.subrequests = subrequests.SubrequestsBase(self.session)
            self.filter = client_2.filter
        else:
            self.log = client.LogAPI(self.session)
            self.asset = client.AssetAPI(self.session)
            self.area = client.AreaAPI(self.session)
            self.term = client.TermAPI(self.session)
            self.info = partial(client.info, self.session)

    def authorize(self, username=None, password=None, scope=None):
        """Authorize with the farmOS server.

        The client must be authorized with the farmOS server before making requests.
        This method utilizes the OAuth Password Credentials flow to authorize users.

        :param username: farmOS Username. Prompted if not included.
        :param password: farmOS Password. Prompted if not included.
        :param scope: Scope to authorize as with the farmOS server. Defaults to "user_access".
        :return: OAuth Token.
        """

        return self.session.authorize(username, password, scope)
