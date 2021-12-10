# Authorization

The farmOS.py client authenticates with the farmOS server via OAuth `Bearer`
tokens. Before authenticating with the server, a farmOS client must be 
created and an OAuth Authorization flow must be completed (unless an optional 
`token` was provided when creating the client).

## Authorizing with Password Credentials (most common)

```python
from farmOS import farmOS

hostname = "myfarm.farmos.net"
username = "username"
password = "password"

# Create the client.
farm_client = farmOS(
    hostname=hostname,
    client_id = "farm", # Optional. The default oauth client_id "farm" is enabled on all farmOS servers.
    scope="farm_manager", # Optional. The default scope is "farm_manager". Only needed if authorizing with a different scope.
    version=2 # Optional. The major version of the farmOS server, 1 or 2. Defaults to 2.
)

# Authorize the client, save the token.
# A scope can be specified, but will default to the default scope set when initializing the client.
token = farm_client.authorize(username, password, scope="farm_manager")
```

Running from a Python Console, the `username` and `password` can also be 
omitted and entered at runtime. This allows testing without saving 
credentials in plaintext:

```python
>>> from farmOS import farmOS
>>> farm_client = farmOS(hostname="myfarm.farmos.net")
>>> farm_client.authorize()
Warning: Password input may be echoed.
Enter username: >? username
Warning: Password input may be echoed.
Enter password: >? password
>>> farm_client.info()
```

## Authorizing with existing OAuth Token (advanced)

An existing token can be provided when creating the farmOS client. This is
useful for advanced use cases where an OAuth token may be persisted.

```python
from farmOS import farmOS

hostname = "myfarm.farmos.net"
token = {
    "access_token": "abcd",
    "refresh_token": "abcd",
    "expires_at": "timestamp",
}

# Create the client with existing token.
farm_client = farmOS(
    hostname=hostname,
    token=token,
)
```

## Saving OAuth Tokens

By default, access tokens expire in 1 hour. This means that requests sent 1 
hour after authorization will trigger a `refresh` flow, providing the client
with a new `access_token` to use. A `token_updater` can be provided to save 
tokens external of the session when automatic refreshing occurs.

The `token_updater` defaults to an empty lambda function: `lambda new_token: None`.
Alternatively, set `token_updater = None` to allow the [`requests_oauthlib.TokenUpdated`](https://requests-oauthlib.readthedocs.io/en/latest/api.html#requests_oauthlib.TokenUpdated)
exception to be raised and caught by code executing requests from farmOS.py.

```python
from farmOS import farmOS

hostname = "myfarm.farmos.net"
username = "username"
password = "password"

# Maintain an external state of the token.
current_token = None

# Callback function to save new tokens.
def token_updater(new_token):
    print(f"Got a new token! {new_token}")
    # Update state.
    current_token = new_token

# Create the client.
farm_client = farmOS(
    hostname=hostname,
    token_updater=token_updater, # Provide the token updater callback.
)

# Authorize the client.
# Save the initial token that is created.
current_token = farm_client.authorize(username, password, scope="farm_manager")
```