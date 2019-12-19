# farmOS.py

[![Licence](https://img.shields.io/badge/Licence-GPL%203.0-blue.svg)](https://opensource.org/licenses/GPL-3.0/)
[![Release](https://img.shields.io/github/release/farmOS/farmOS.py.svg?style=flat)](https://github.com/farmOS/farmOS.py/releases)
[![Last commit](https://img.shields.io/github/last-commit/farmOS/farmOS.py.svg?style=flat)](https://github.com/farmOS/farmOS.py/commits)
[![Twitter](https://img.shields.io/twitter/follow/farmOSorg.svg?label=%40farmOSorg&style=flat)](https://twitter.com/farmOSorg)
[![Chat](https://img.shields.io/matrix/farmOS:matrix.org.svg)](https://riot.im/app/#/room/#farmOS:matrix.org)

farmOS.py is a Python library for interacting with [farmOS](https://farmOS.org)
over API.

For more information on farmOS, visit [farmOS.org](https://farmOS.org).

## USAGE

    import farmOS

    hostname = 'myfarm.farmos.net'
    username = 'My Name'
    password = 'mYPa$$w0rd'

    farm = farmOS.farmOS(hostname, username, password)
    success = farm.authenticate()

    # Get farm info
    info = farm.info()

    # Get all logs
    logs = farm.log.get()
    # Get harvest logs
    harvests = farm.log.get({
      'type':'farm_harvest'
      })
    # Get log number 37
    log = farm.log.get(37)

    # Get all assets
    assets = farm.asset.get()
    # Get all animal assets
    animals = farm.asset.get({
      'type':'animal'
      })

    # Get all areas
    areas = farm.area.get()
    # Get field areas
    fields = farm.area.get({
      'area_type':'field'
      })

    # Get all terms
    terms = farm.term.get()
    # Get all terms from farm_crops vocabulary
    crops = farm.term.get('farm_crops')

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
