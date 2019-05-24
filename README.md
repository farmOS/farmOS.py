# farmOS.py

[![Licence](https://img.shields.io/badge/Licence-GPL%203.0-blue.svg)](https://opensource.org/licenses/GPL-3.0/)
[![Release](https://img.shields.io/github/release/farmOS/farmOS.svg?style=flat)](https://github.com/farmOS/farmOS-aggregator/releases)
[![Last commit](https://img.shields.io/github/last-commit/farmOS/farmOS.svg?style=flat)](https://github.com/farmOS/farmOS-aggregator/commits)
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
    animals = farm.log.get({
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

## TESTING
Configure credentials for the farmOS instance used to test in

    tests/test_credentials.py

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
