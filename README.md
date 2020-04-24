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

#### OAuth (Added in v0.1.6)

Support for OAuth was added to [farmOS.py] starting with v0.1.6. To authorize
and authenticate via OAuth, just supply the required parameters when creating
a client. The library will know to use an OAuth Password Credentials or 
Authorization Code flow.

##### OAuth Password Credentials (most common)

```python
from farmOS import farmOS

hostname = "myfarm.farmos.net"
username = "username"
password = "password"

farm_client = farmOS(
    hostname=hostname,
    username=username,
    password=password,
    client_id = "farm", # The default oauth client_id enabled on all farmOS servers.
    # scope="farm_info" # The default scope is "user_access". Only needed if testing different scope.
)
```

Running from a Python Console, the `password` can also be omitted and entered
at runtime. This allows testing without saving a password in plaintext:

```python
>>> from farmOS import farmOS
>>> farm_client = farmOS(hostname=hostname, username=username, client_id="farm")
>>> Warning: Password input may be echoed.
>>> Enter password: >? MY_PASSWORD
>>> farm_client.info()
'name': 'server-name', 'url': 'http://localhost', 'api_version': '1.2', 'user': ....
```

##### OAuth Authorization Flow (advanced)

It's also possible to run the Authorization Code Flow from the Python console.
This is great way to test the Authorization process users will go through. The
console will print a link to navigate to where you sign in to farmOS and 
complete the authorization process. You then copy the `link` from the page you
are redirected to back into the console. This supplies the `farm_client` with
an an authorization `code` that it uses to request an OAuth `token`. 

```python
>>> farm_client = farmOS(hostname=hostname, client_id="farm")
Please go here and authorize, http://localhost/oauth2/authorize?response_type=code&client_id=farmos_development&redirect_uri=http%3A%2F%2Flocalhost%2Fapi%2Fauthorized&scope=user_access&state=V9RCDd4yrSWZP8iGXt6qW51sYxsFZs&access_type=offline&prompt=select_account
Paste the full redirect URL here:>? http://localhost/api/authorized?code=33429f3530e36f4bdf3c2adbbfcd5b7d73e89d5c&state=V9RCDd4yrSWZP8iGXt6qW51sYxsFZs
>>> farm_client.info()
'name': 'server-name', 'url': 'http://localhost', 'api_version': '1.2', 'user': ....
```

##### Saving OAuth Tokens

farmOS.py can save OAuth Tokens to a config file so that they can be used at a
later time. To do this, supply a `config_file` and `profile_name` to save the
connection info under.

```python
from farmOS import farmOS

hostname = "myfarm.farmos.net"
username = "username"
password = "password"

farm_client = farmOS(
    hostname=hostname,
    username=username,
    password=password,
    client_id="farm", # The default oauth client_id enabled on all farmOS servers.
    config_file="farmos_config.cfg",    
    profile_name="My farmOS Server"
)
```

After initial connection, the config will be saved to `profile_name` in `config_file`.

Later authentication can then simply be done by supplying just the `config_file` and
`profile_name` when creating a farmOS client (as long as OAuth tokens have not expired):

```python
from farmOS import farmOS

farm_client = farmOS(
    config_file="farmos_config.cfg",    
    profile_name="My farmOS Server"
)
```

#### Drupal Auth

Simple one-time communication to the farmOS server can be completed via Drupal Auth:

```python
from farmOS import farmOS

hostname = "myfarm.farmos.net"
username = "username"
password = "password"

farm_client = farmOS(
    hostname=hostname,
    username=username,
    password=password,
)
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
