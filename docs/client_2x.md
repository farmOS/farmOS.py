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
- `resource.get()`: Perform a GET request. Returns a single page of resources.
- `resource.get_id()`: Perform a GET request for a single resource.
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

#### `.get()` and `.get_id()`

```python
# Get one page of observation logs.
response = farm_client.log.get('observation')

# Filter to 'done' logs.
filters = farm_client.filter('status', 'done')
response = farm_client.log.get('observation', params=filters)

# Get observation log by ID.
id = 'b9e8c253-a3c1-4af4-b2c8-7f201dc2b046'
log = farm_client.log.get_id('observation', id)
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

#### `.get()` and `.get_id()`

```python

# Get one page of animal assets.
response = farm_client.asset.get('animal')

# Filter to female animals.
filters = farm_client.filter('sex', 'f')
response = farm_client.asset.get('animal', params=filters)

# Get asset by ID.
response = farm_client.asset.get_id('animal', 'b9e8c253-a3c1-4af4-b2c8-7f201dc2b046')
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

#### `.get()` and `.get_id()`

```python

# Get one page of plant_type terms
response = farm_client.term.get('plant_type')

# Get a specific term
response = farm_client.term.get_id('plant_type', "a260441b-2553-4715-83ee-3ac08a6b85f0")
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