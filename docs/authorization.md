# Authorization

## Background

farmOS includes an OAuth2 Authorization server for providing 1st and 3rd party
clients access to the farmOS API. For more information on the OAuth2
specification see the [farmOS API authentication documentation](https://farmos.org/development/api/authentication/).

farmOS.py provides a `FarmClient` wrapper around the [HTTPX](https://www.python-httpx.org/)
HTTP Python client and uses the [HTTPX-Auth](https://github.com/Colin-b/httpx_auth)
library for OAuth2 authentication. For advanced use-cases that require other
authentication schemes see [HTTPX custom authentication schemes](https://www.python-httpx.org/advanced/authentication/#custom-authentication-schemes).

## OAuth2 Authorization Flow

Before making requests to the farmOS server an OAuth2 client and grant must be
configured on the farmOS server to be used in an OAuth2 authorization flow.

An OAuth Client represents a 1st or 3rd party integration with the farmOS
server. Clients are uniquely identified by a `client_id` and can have an
optional `client_secret` for private integrations. Clients are configured
to allow only specific OAuth grants and can specify default scopes that
are granted when none are requested.

The OAuth2 Password Credentials Flow is documented here because most Python
scripting use-cases can be trusted with a username and password (considered
a 1st party client). The core `farm_api_default_consumer` module provides a
default client with `client_id = farm` that can use the `password` grant. You
can use this client for general usage of the API, like writing a script that
communicates with your farmOS server, but it comes with limitations. For more
information on OAuth2 authorization flows supported by the farmOS server see the
[farmOS Authorization Flow documentation](https://farmos.org/development/api/authentication/#authorization-flows).

## Usage in farmOS.py

Instantiate an OAuth2 flow from the HTTPX-Auth library. Pass this to the
`FarmClient` using the `auth` parameter:

```python
from httpx_auth import OAuth2ResourceOwnerPasswordCredentials
from farmOS import FarmClient

FARMOS_HOSTNAME="https://myfarm.farmos.net"

auth = OAuth2ResourceOwnerPasswordCredentials(
    token_url=f"{FARMOS_HOSTNAME}/oauth/token",
    username=USERNAME,
    password=PASSWORD,
    client_id="farm",
    scope="farm_manager",
)
farm_client = FarmClient(hostname=FARMOS_HOSTNAME, auth=auth)
```