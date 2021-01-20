# farmOS.py

[![Licence](https://img.shields.io/badge/Licence-GPL%203.0-blue.svg)](https://opensource.org/licenses/GPL-3.0/)
[![Release](https://img.shields.io/github/release/farmOS/farmOS.py.svg?style=flat)](https://github.com/farmOS/farmOS.py/releases)
[![Last commit](https://img.shields.io/github/last-commit/farmOS/farmOS.py.svg?style=flat)](https://github.com/farmOS/farmOS.py/commits)
[![Twitter](https://img.shields.io/twitter/follow/farmOSorg.svg?label=%40farmOSorg&style=flat)](https://twitter.com/farmOSorg)
[![Chat](https://img.shields.io/matrix/farmOS:matrix.org.svg)](https://riot.im/app/#/room/#farmOS:matrix.org)

farmOS.py is a Python library for interacting with [farmOS](https://farmOS.org)
over API.

For more information on farmOS, visit [farmOS.org](https://farmOS.org).

- [Installation](#installation)
- [Usage](#usage)
  - [Authentication](#authentication)
    - [OAuth](#OAuth)
     - [OAuth Password Credentials](#oauth-password-credentials-most-common)
     - [OAuth Authorization Flow](#oauth-authorization-flow-advanced)
     - [Saving OAuth Tokens](#saving-oauth-tokens)
  - [Server Info](#server-info)
  - [Client methods](#client-methods)  
    - [farmOS 1.x](docs/client_1x.md)
    - [farmOS 2.x](docs/client_2x.md)
  - [Logging](#logging)


## Installation

To install using pip:

```bash
$ pip install farmOS
```

## Usage

### Authentication

The farmOS.py client authenticates with the farmOS server via OAuth `Bearer`
tokens. Before authenticating with the server, a farmOS client must be 
created and an OAuth Authorization flow must be completed (unless an optional 
`token` was provided when creating the client).

##### Authorizing with Password Credentials (most common)

```python
from farmOS import farmOS

hostname = "myfarm.farmos.net"
username = "username"
password = "password"

# Create the client.
farm_client = farmOS(
    hostname=hostname,
    client_id = "farm", # Optional. The default oauth client_id "farm" is enabled on all farmOS servers.
    scope="user_access", # Optional. The default scope is "user_access". Only needed if authorizing with a different scope.
    version=1 # Optional. The major version of the farmOS server, 1 or 2. Defaults to 1.
)

# Authorize the client, save the token.
token = farm_client.authorize(username, password, scope="user_access")
```

Running from a Python Console, the `username` and `password` can also be 
omitted and entered at runtime. This allows testing without saving 
credentials in plaintext:

```python
>>> from farmOS import farmOS
>>> farm_client = farmOS(hostname="myfarm.farmos.net", client_id="farm", scope="user_access")
>>> farm_client.authorize()
Warning: Password input may be echoed.
Enter username: >? username
Warning: Password input may be echoed.
Enter password: >? password
>>> farm_client.info()
'name': 'server-name', 'url': 'http://localhost', 'api_version': '1.2', 'user': ....
```

##### Authorizing with existing OAuth Token (advanced)

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

##### Saving OAuth Tokens

By default, `access_tokens` expire in 1 hour. This means that requests sent 
1 hour after authorization will trigger a `refresh` flow, providing the 
client with a new `access_token` to use. A `token_updater` utility must be 
provided to save tokens when automatic refreshing occurs. 

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
current_token = farm_client.authorize(username, password, scope="user_access")
```

### Server Info

```python

info = farm_client.info()

{
    'name': 'farmos-test',
    'url': 'http://localhost',
    'api_version': '1.2',
    'user': {
        'uid': '4',
        'name': 'paul',
        'mail': 'paul.weidner+2@gmail.com'
    },
    'google_maps_api_key': 'AIzaSyCCHTbAGC_gHegwepMxBu_AKd_RmP54mDg',
    'metrics': {
        'equipment': {'label': 'Equipment', 'value': '7', 'link': 'farm/assets/equipment/list', 'weight': 0},
        'areas': {'label': 'Areas', 'value': '20', 'link': 'farm/areas', 'weight': 100},
        'field': {'label': 'Field area', 'value': '532 hectares', 'link': 'farm/areas', 'weight': 101}
    },
    'system_of_measurement': 'metric',
}
```


### Client methods

farmOS.py can connect to farmOS servers running version ^1.6 or 2.x. The version should be specified when instantiating
the farmOS client, see [Authentication](#authentication).

Because of [API changes](https://2x.farmos.org/development/api/changes/) in farmOS 2.x, the client provides different
methods depending on the server version:

- [1.x methods](docs/client_1x.md)
- [2.x methods](docs/client_2x.md)

### Logging

You can configure how `farmOS` logs are displayed with the following:
```python
import logging

# Required to init a config on the ROOT logger, that all other inherit from
logging.basicConfig()

 # Configure all loggers under farmOS (farmOS.client, famrOS.session) to desired level
logging.getLogger("farmOS").setLevel(logging.DEBUG)

 # Hide debug logging from the farmOS.session module
logging.getLogger("farmOS.session").setLevel(logging.WARNING)
```
More info on logging in Python [here](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial).

## TESTING
Functional tests require a live instance of farmOS to communicate with.
Configure credentials for the farmOS instance to test against by setting the following environment variables: 

For farmOS Drupal Authentication:
`FARMOS_HOSTNAME`, `FARMOS_RESTWS_USERNAME`, and `FARMOS_RESTWS_PASSWORD`

For farmOS OAuth Authentication (Password Flow):
`FARMOS_HOSTNAME`, `FARMOS_OAUTH_USERNAME`, `FARMOS_OAUTH_PASSWORD`, `FARMOS_OAUTH_CLIENT_ID`, `FARMOS_OAUTH_CLIENT_SECRET`

Automated tests are run with pytest

    python setup.py test

## MAINTAINERS

 * Paul Weidner (paul121) - https://github.com/paul121
 * Michael Stenta (m.stenta) - https://github.com/mstenta

This project has been sponsored by:

 * [Farmier](https://farmier.com)
 * [Pennsylvania Association for Sustainable Agriculture](https://pasafarming.org)
 * [Our Sci](http://our-sci.net)
 * [Bionutrient Food Association](https://bionutrient.org)
 * [Foundation for Food and Agriculture Research](https://foundationfar.org/)
