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
  - [Logs](#logs)
    - [`.get()`](#get)
    - [`.send()`](#send)
    - [`.delete()`](#delete)
  - [Assets](#assets)
    - [`.get()`](#get-1)
    - [`.send()`](#send-1)
    - [`.delete()`](#delete-1)
  - [Areas](#areas)
    - [`.get()`](#get-2)
    - [`.send()`](#send-2)
    - [`.delete()`](#delete-2)
  - [Taxonomy Terms](#taxonomy-terms)
    - [`.get()`](#get-3)
    - [`.send()`](#send-3)
    - [`.delete()`](#delete-3)
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
    scope="user_access" # Optional. The default scope is "user_access". Only needed if authorizing with a differnt scope.
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

### Logs


A log is any type of event that occurs on the farm, from a planting to a harvest
to just a general observation.

Methods for getting, sending and deleting logs are namespaced on the `farm.log`
property.

#### `.get()`

```python
# Get all logs
logs = farm_client.log.get()['list']

# Get harvest logs
filters = {
    'type': 'farm_harvest'
}

harvests = farm_client.log.get(filters=filters)['list']

# Get log number 37
log = farm_client.log.get(37)
```

The four default log types are:

- `farm_activity`
- `farm_harvest`
- `farm_input`
- `farm_observation`

Other log types may be provided by add-on modules in farmOS.

#### `.send()`

Send can be used to create a new log, or if the `id` property is included, to
update an existing log:

```python

# Create observation log
observation_log = {
  "name": "My Great Planting",
  "type": "farm_observation",
  "done": 0,
  "notes": "Some notes"    
}
log = farm_client.log.send(log)

# Mark log 35 as done
done = {
    'id': 45,
    'done': 1
}
log = farm_client.log.send(done)
```

#### `.delete()`

```python
farm_client.log.delete(123)
```

### Assets

Assets are any piece of property or durable good that belongs to the farm, such
as a piece of equipment, a specific crop, or an animal.

Methods for getting, sending and deleting assets are namespaced on the
`farm.asset` property.

#### `.get()`

```python

# Get all assets
assets = farm_client.asset.get()['list']

# Get all animal assets
filters = {
  'type':'animal'
}
animals = farm_client.asset.get(filters=filters)['list']

# Get asset ID 45
asset = farm_client.asset.get(45)
```

Some common asset types include:

- `animal`
- `equipment`
- `planting`

Other asset types may be provided by add-on modules in farmOS.

#### `.send()`

Send can be used to create a new asset, or if the `id` property is included, to update an existing asset:

```python

planting_asset = {
  "name": "My Great Planting",
  "type": "planting",
  "crop": [
    {"id": 8} # Crop term id
  ]
}

asset = farm_client.asset.send(planting_asset)
```

#### `.delete()`

```python
farm_client.asset.delete(123)
```

### Areas

An area is any well defined location that has been mapped in farmOS, such as a field, greenhouse, building, etc.

Here's an example of what an area looks like as a Python dict:

```python
{
  'tid': '22',
  'name': 'F1',
  'description': '',
  'area_type': 'greenhouse',
  'geofield': [
    {
      'geom': 'POLYGON ((-75.53640916943549 42.54421203378203, -75.53607389330863 42.54421796218091, -75.53607121109961 42.54415472589722, -75.53640648722647 42.54414682135726, -75.53640916943549 42.54421203378203))',
    }
  ],
  'vocabulary': {
    'id': '2',
    'resource': 'taxonomy_vocabulary'
  },
  'parent': [
    {
      'id': 11,
      'resource': 'taxonomy_term'
    }
  ],
  'weight': '0',
}
```

Methods for getting, sending and deleting areas are namespaced on the `farm.area` property.

#### `.get()`

```python

# Get all areas
areas = farm_client.area.get()['list']

# Get field areas
filters = {
  'area_type':'field'
}
fields = farm_client.area.get(filters=filters)['list']

# Get area with tid 37
area = farm_client.area.get(37)
```

__NOTE:__ Areas use a `tid` property, unlike logs and assets which have an `id`. This stands for taxonomy ID. In the future this may be changed to make it more consistent with the other entities.

Some common area types include:

- `field`
- `building`
- `property`
- `water`
- `other`

Other area types may be provided by add-on modules in farmOS.

#### `.send()`

Send can be used to create a new area, or if the `tid` property is included, to update an existing area:

```python



```

#### `.delete()`

```python
farm_client.area.delete(123)
```

### Taxonomy Terms

farmOS allows farmers to build vocabularies of terms for various categorization
purposes. These are referred to as "taxonomies" in farmOS (and Drupal), although
"vocabulary" is sometimes used interchangeably.

Some things that are represented as taxonomy terms include quantity units,
crops/varieties, animal species/breeds, input materials, and log categories.
See "Endpoints" above for specific API endpoints URLs.

A very basic taxonomy term JSON structure looks like this:

```json
{
  "tid": "3",
  "name": "Cabbage",
  "description": "",
  "vocabulary": {
    "id": "7",
    "resource": "taxonomy_vocabulary",
  },
  "parent": [
    {
      "id": "10",
      "resource": "taxonomy_term",
    },
  ],
  "weight": "5",
}
```

The `tid` is the unique ID of the term (database primary key). When creating a
new term, the only required fields are `name` and `vocabulary`. The vocabulary
is an ID that corresponds to the specific vocabulary the term will be a part of
(eg: quantity units, crops/varieties, log categories, etc). The fields `parent`
and `weight` control term hierarchy and ordering (a heavier `weight` will sort
it lower in the list).

#### `.get()`

```python

# Get all terms
terms = farm_client.term.get()['list']

# Get all terms from farm_crops vocabulary
crops = farm_client.term.get('farm_crops')['list']

# Get term ID 67
term = farm_client.term.get(67)
```

#### `.send()`

Send can be used to create a new taxonomy term, or if the `tid` property is included in the term object, to update an existing area:

```python

```

#### `.delete()`

```python
farm_client.term.delete(56)
```

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
