# Subrequests

## Background

farmOS.py supports the [Subrequests](https://www.drupal.org/project/subrequests) module included with a farmOS server.

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

## Example 

An example that creates a new asset followed by a new log that references the asset:
  
```python
from farmOS import farmOS
from farmOS.subrequests import Action, Subrequest, SubrequestsBlueprint, Format

client = farmOS("http://localhost", scope="farm_manager", version=2)
client.authorize('username', 'password')

plant_type = {
    "data": {
        "type": "taxonomy_term--plant_type",
        "attributes": {
            "name": "New plant type"
        }
    }
}

new_plant_type = Subrequest(action=Action.create, requestId="create-plant-type", endpoint="api/taxonomy_term/plant_type", body=plant_type)

plant = {
    "data": {
        "type": "asset--plant",
        "attributes": {
            "name": "My new plant",
            "notes": "Created in the first request.",
        },
        "relationships": {
            "plant_type": {
                "data": [
                    {
                        "type": "taxonomy_term--plant_type",
                        "id": "{{create-plant-type.body@$.data.id}}"
                    }
                ]
            }
        }
    }
}
new_asset = Subrequest(action=Action.create, requestId="create-asset", waitFor=["create-plant-type"], endpoint="api/asset/plant", body=plant)

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
blueprint = SubrequestsBlueprint.parse_obj([new_plant_type, new_asset, new_log])

# OR provide a list of Subrequest objects.
blueprint = [new_plant_type, new_asset, new_log]

# Send the blueprint.
response = client.subrequests.send(blueprint, format=Format.json)
```
