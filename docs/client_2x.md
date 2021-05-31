# Client methods for farmOS 2.x

- [Resources](#resources)
  - [Logs](#logs)
  - [Assets](#assets)
  - [Taxonomy Terms](#taxonomy-terms)
- [Subrequests](#subrequests)

## Resources

The farmOS 2.x API uses the JSON:API module included with Drupal core, which 
follows the [JSON:API](https://jsonapi.org/) specification for defining API 
resources. More info on the farmOS 2.x api 
[here](https://2x.farmos.org/development/api/).

Any resource on a farmOS 2.x server can be interacted via the
`farm_client.resource` namespace in the farmOS.py client. The following methods
are available:
- `resource.get()`: Perform a GET request.
- `resource.iterate()`: Returns a Python iterator that can be used to GET
  multiple pages of resources.
- `resource.send()`: Perform a POST or PATCH request.
- `resource.delete()`: Perform a DELETE request.

Each of these methods requires the JSON:API resource type identifier in order 
to determine the correct URL of the resource. Because the Drupal JSON:API module
implements JSON:API resources in the format `{entity_type}--{bundle}`,
the resource type identifier is supplied to each method with two arguments:
`entity_type` and `bundle`.

```python
# Get log--observation resources.
response = farm_client.resource.get('log', 'observation')
```

It's also possible for Drupal entities to not have a bundle, as is the case 
with the `user` entity. For these entities the resource identifier is in the
format `{entity_type}--{entity_type}`. For convenience, if the `bundle` is not
provided, it assumed the entity has no bundles:

```python
# Get user--user resources.
response = farm_client.resource.get('user')
```

Similarly, Logs, Assets and Terms have these same methods available within
their own namespace and only require the `bundle` parameter.
    
### Logs

A log is any type of event that occurs on the farm, from a planting to a 
harvest to just a general observation.

Methods for getting, sending and deleting logs are namespaced on the `farm.log`
property.

The four default log types are:

- `activity`
- `harvest`
- `input`
- `observation`

Other log types may be provided by add-on modules in farmOS.

#### `.iterate()`

```python
# Get all observation logs.
logs = list(farm_client.log.iterate('observation'))

# Filter to 'done' logs.
filters = farm_client.filter('status', 'done')
done_observations = list(farm_client.log.iterate('observation', params=filters))
```

#### `.get()`

```python
# Get one page of observation logs.
response = farm_client.log.get('observation')

# Filter to 'done' logs.
filters = farm_client.filter('status', 'done')
response = farm_client.log.get('observation', params=filters)

# Get observation log by ID.
id = 'b9e8c253-a3c1-4af4-b2c8-7f201dc2b046'
log = farm_client.log.get('observation', id)
```

#### `.send()`

Send can be used to create a new log, or if the `id` property is included, to
update an existing log:

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

# Update log.
done = {
    'id': 'b9e8c253-a3c1-4af4-b2c8-7f201dc2b046',
    "attributes": {
        "status": "done",
    }
}
log = farm_client.log.send('observation', done)
```

#### `.delete()`

```python
farm_client.log.delete('observation', 'b9e8c253-a3c1-4af4-b2c8-7f201dc2b046')
```

### Assets

Assets are any piece of property or durable good that belongs to the farm, such
as a piece of equipment, a specific crop, or an animal.

Methods for getting, sending and deleting assets are namespaced on the
`farm.asset` property.

### `.iterate()`

```python
# Get all animal assets.
logs = list(farm_client.asset.iterate('animal'))

# Filter to female animals.
filters = farm_client.filter('sex', 'f')
females = list(farm_client.asset.iterate('animal', params=filters))
```

#### `.get()`

```python

# Get one page of animal assets.
response = farm_client.asset.get('animal')

# Filter to female animals.
filters = farm_client.filter('sex', 'f')
response = farm_client.asset.get('animal', params=filters)

# Get asset by ID.
response = farm_client.asset.get('animal', 'b9e8c253-a3c1-4af4-b2c8-7f201dc2b046')
```

Some common asset types include:

- `land`
- `structure`  
- `water`  
- `animal`
- `plant`
- `equipment`
- `sensor`

Other asset types may be provided by add-on modules in farmOS.

#### `.send()`

Send can be used to create a new asset, or if the `id` property is included, to update an existing asset:

```python

# Create a plant asset.
plant_asset = {
    "attributes": {
        "name": "My Great Planting",
    },
    "relationships": {
        "plant_type": {
            "data": [
                {
                    "type": "taxonomy_term--plant_type",
                    "id": "a260441b-2553-4715-83ee-3ac08a6b85f0",
                },
            ],
        },
    },
}

response = farm_client.asset.send('plant', plant_asset)

# Update planting.
update = {
    'id': response["data"]["id"],
    "attributes": {
        "status": "archived",
    }
}
response = farm_client.asset.send('plant', update)
```

#### `.delete()`

```python
farm_client.asset.delete('planting', "b9e8c253-a3c1-4af4-b2c8-7f201dc2b046")
```

### Taxonomy Terms

farmOS allows farmers to build vocabularies of terms for various categorization
purposes. These are referred to as "taxonomies" in farmOS (and Drupal), although
"vocabulary" is sometimes used interchangeably.

Some things that are represented as taxonomy terms include quantity units,
crops/varieties, animal species/breeds, input materials, and log categories.

### `.iterate()`

```python
# Get all plant_type terms.
plant_types = list(farm_client.term.iterate('plant'))
```

#### `.get()`

```python

# Get one page of plant_type terms
response = farm_client.term.get('plant_type')

# Get a specific term
response = farm_client.term.get('plant_type', "a260441b-2553-4715-83ee-3ac08a6b85f0")
```

#### `.send()`

Send can be used to create a new taxonomy term, or if the `id` property is included, to update an existing term:

```python
# Create a new plant type.
response = farm_client.term.send('plant_type', {"attributes": {"name": "Corn"}})
```

#### `.delete()`

```python
farm_client.term.delete('plant_type', "a260441b-2553-4715-83ee-3ac08a6b85f0")
```

## Subrequests

farmOS.py supports the [Subrequests](https://www.drupal.org/project/subrequests) module which can optionally be 
installed on the farmOS server.

Subrequests allows multiple requests to be defined in a "blueprint" and sent to the server in a single POST request. 
The blueprint can define sequential requests so that the response of one request can be embedded into the body of a 
later request. See the subrequests [blueprint specification](https://git.drupalcode.org/project/subrequests/blob/8.x-2.x/SPECIFICATION.md)
for more documentation.

farmOS.py provides some additional features to help use subrequests:
- The default response format is set to `json` by appending a `?_format=json` query parameter automatically. JSON is 
  much easier to parse than subrequest's default `html` format, but HTML can be requested by specifying `format='html'`.
- Unless otherwise provided, the `Accept` and `Content-Type` headers for each sub-request will be set to
  `application/vnd.api+json` for standard JSONAPI requests.
- An `endpoint` can be provided instead of the full `uri` for each sub-request. farmOS.py will build the full `uri` 
  from the `hostname` already configured with the client.
- The sub-request `body` can be provided as an object that farmOS.py will serialize into a JSON object string.
- Blueprints are validated using Pydantic models. These models can also be used to build individual requests to include
  in a blueprint.
  
An example that creates a new asset followed by a new log that references the asset:
  
```python
from farmOS import farmOS
from farmOS.subrequests import Action, Subrequest, SubrequestsBlueprint, Format

client = farmOS("http://localhost", scope="farm_manager", version=2)
client.authorize(username, password)

plant = {
    "data": {
        "type": "asset--plant",
        "attributes": {
            "name": "My new plant",
            "description": "Created in the first request.",
        },
    }
}
new_asset = Subrequest(action=Action.create, requestId="create-asset", endpoint="api/asset/plant", body=plant)

log = {
    "data": {
        "type": "log--seeding",
        "attributes": {
            "name": "Seeding my new plant",
            "notes": "Created in the second request.",
        },
        "relationships": {
            "asset": {
                "data": [
                    {
                        "type": "asset--plant",
                        "id": "{{create-asset.body@$.data.id}}"
                    }
                ]
            }
        }
    }
}
new_log = Subrequest(action=Action.create, requestId="create-log", waitFor=["create-asset"], endpoint="api/log/seeding", body=log)

# Create a blueprint object
blueprint = SubrequestsBlueprint.parse_obj([new_asset, new_log])

# OR provide a list of Subrequest objects.
blueprint = [new_asset, new_log]

# Send the blueprint.
response = client.subrequests.send(blueprint, format=Format.json)

# New resource ids.
print(response['create-asset']['data']['id'])
print(response['create-log']['data']['id'])
```
