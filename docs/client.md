# Client methods for farmOS

## Resources

The farmOS API uses the JSON:API module included with Drupal core, which 
follows the [JSON:API](https://jsonapi.org/) specification for defining API 
resources. More information on the farmOS api see the
[farmOS API documentation](https://farmos.org/development/api/).

Any resource on a farmOS server can be interacted via the
`farm_client.resource` namespace in the farmOS.py client. The following methods
are available:
- `resource.get(entity_type, bundle, params)`: Perform a GET request. Returns a single page of resources.
- `resource.get_id(entity_type, bundle, id)`: Perform a GET request for a single resource.
- `resource.iterate(entity_type, bundle, params)`: Returns a Python iterator that can be used to GET
  multiple pages of resources.
- `resource.send(entity_type, bundle, payload)`: Perform a POST or PATCH request.
- `resource.delete(entity_type, bundle, id)`: Perform a DELETE request.

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

For convenience, Logs, Assets and Terms have these same methods available
within their own namespace and only require the `bundle` parameter. To
interact with Logs:
- `farm_client.log.get('observation')`
- `farm_client.log.get_id('observation', log_id)`
- `farm_client.log.iterate('observation')'`
- `farm_client.log.send('observation', log_data)`
- `farm_client.log.delete('observation', log_id)`
    
### Resource methods

Below are examples interacting with assets.

Assets are any piece of property or durable good that belongs to the farm, such
as a piece of equipment, a specific crop, or an animal.

Methods for getting, sending and deleting assets are namespaced on the
`farm.asset` property.

#### `.iterate()`

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