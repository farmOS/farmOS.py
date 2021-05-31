# Client methods for farmOS 1.x 

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
