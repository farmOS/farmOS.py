# Introduction

## Motivation

farmOS.py is a Python library for interacting with farmOS servers over API.

This library was developed to support more custom use cases that interact 
with the farmOS server from a Python scripting environment. It can be used
to build custom importers and exporters that interface with CSV, IoT and
other APIs. farmOS.py also helps integrate with existing scientific and GIS
tools that exist in the Python ecosystem.

## Quick start

Learn farmOS.py by example.

### 1. Install 

To install using `pip`:

```bash
$ pip install farmOS
```

To install using `conda` see [conda-forge/farmos-feedstock](https://github.com/conda-forge/farmos-feedstock#installing-farmos)

### 2. Create a FarmClient instance

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

### 3. Get farmOS server info

```python
info = farm_client.info()
```

### 4. CRUD Operations with a farmOS log

```python

# Create observation log
observation_log = {
    "attributes": {
        "name": "My Great Observation",
        "status": "pending",
        "notes": "Some notes"       
    } 
}
log = farm_client.log.send('observation', observation_log)
log_id = log["data"]["id"]

# Update the log status to "done".
done = {
    'id': log_id,
    "attributes": {
        "status": "done",
    }
}
updated_log = farm_client.log.send('observation', done)

# Delete the log.
farm_client.log.delete('observation', log_id)
```

## Next steps

Now that you know the basics, dive deeper into following topics:

- [Authorizing with farmOS server](authorization.md)
- [Working with farmOS resources](client.md)
- [Async Support](async.md)
- [Using Subrequests](subrequests.md)
