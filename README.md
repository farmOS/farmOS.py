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

    logs = farm.get_records('log')
    harvests = farm.get_records(log', filters={'type':'farm_harvest'}')
    areas = farm.get_areas()

## TESTING
Configure credentials for the farmOS instance used to test in

    tests/test_credentials.py

Automated tests are run with pytest

    python setup.py test

## MAINTAINERS

 * Michael Stenta (m.stenta) - https://github.com/mstenta

This project has been sponsored by:

 * [Farmier](https://farmier.com)
 * [Pennsylvania Association for Sustainable Agriculture](https://pasafarming.org)
 * [Our Sci](http://our-sci.net)
 * [Bionutrient Food Association](https://bionutrient.org)
 * [Foundation for Food and Agriculture Research](https://foundationfar.org/)

