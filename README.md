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
  - [Server Info](#server-info)
  - [Client methods](#client-methods)  
    - [farmOS 1.x](docs/client_1x.md)
    - [farmOS 2.x](docs/client_2x.md)


## Installation

To install using `pip`:

```bash
$ pip install farmOS~=1.0.0b
```

To install using `conda` see [conda-forge/farmos-feedstock](https://github.com/conda-forge/farmos-feedstock#installing-farmos)

## Usage

### Server Info

```python

info = farm_client.info()

{
  "jsonapi": {
    "version": "1.0",
    "meta": {
      "links": {
        "self": {
          "href": "http://jsonapi.org/format/1.0/"
        }
      }
    }
  },
  "data": [],
  "meta": {
    "links": {
      "me": {
        "meta": {
          "id": "163c6e73-46fb-4283-b26b-153b598151ce"
        },
        "href": "http://localhost/api/user/user/163c6e73-46fb-4283-b26b-153b598151ce"
      }
    },
    "farm": {
      "name": "Drush Site-Install",
      "url": "http://localhost",
      "version": "2.x",
      "system_of_measurement": "metric"
    }
  },
  "links": {
    "asset--animal": {
      "href": "http://localhost/api/asset/animal"
    },
    "asset--equipment": {
      "href": "http://localhost/api/asset/equipment"
    },
    ...
  }
}
```


### Client methods

farmOS.py can connect to farmOS servers running version ^1.6 or 2.x. The version should be specified when instantiating
the farmOS client, see [Authentication](#authentication).

Because of [API changes](https://2x.farmos.org/development/api/changes/) in farmOS 2.x, the client provides different
methods depending on the server version:

- [1.x methods](docs/client_1x.md)
- [2.x methods](docs/client_2x.md)

## MAINTAINERS

 * Paul Weidner (paul121) - https://github.com/paul121
 * Michael Stenta (m.stenta) - https://github.com/mstenta

This project has been sponsored by:

 * [Farmier](https://farmier.com)
 * [Pennsylvania Association for Sustainable Agriculture](https://pasafarming.org)
 * [Our Sci](http://our-sci.net)
 * [Bionutrient Food Association](https://bionutrient.org)
 * [Foundation for Food and Agriculture Research](https://foundationfar.org/)
