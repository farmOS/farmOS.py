import json
from datetime import datetime, timezone

import pytest

from farmOS import FarmClient
from farmOS.subrequests_model import Action, Format, Subrequest, SubrequestsBlueprint
from tests.conftest import farmOS_testing_server

curr_time = datetime.now(timezone.utc)
timestamp = curr_time.isoformat(timespec="seconds")



@farmOS_testing_server
def test_subrequests(farm_auth):
    plant_type = {
        "data": {
            "type": "taxonomy_term--plant_type",
            "attributes": {"name": "New plant type"},
        }
    }

    new_plant_type = Subrequest(
        action=Action.create,
        requestId="create-plant-type",
        endpoint="api/taxonomy_term/plant_type",
        body=plant_type,
    )

    plant = {
        "data": {
            "type": "asset--plant",
            "attributes": {
                "name": "My new plant",
            },
            "relationships": {
                "plant_type": {
                    "data": [
                        {
                            "type": "taxonomy_term--plant_type",
                            "id": "{{create-plant-type.body@$.data.id}}",
                        }
                    ]
                }
            },
        }
    }
    new_asset = Subrequest(
        action=Action.create,
        requestId="create-asset",
        waitFor=["create-plant-type"],
        endpoint="api/asset/plant",
        body=plant,
    )

    log = {
        "data": {
            "type": "log--seeding",
            "attributes": {
                "name": "Seeding my new plant",
            },
            "relationships": {
                "asset": {
                    "data": [
                        {
                            "type": "asset--plant",
                            "id": "{{create-asset.body@$.data.id}}",
                        }
                    ]
                }
            },
        }
    }
    new_log = Subrequest(
        action=Action.create,
        requestId="create-log",
        waitFor=["create-asset"],
        endpoint="api/log/seeding",
        body=log,
    )

    # Create a blueprint object
    blueprint = SubrequestsBlueprint([new_plant_type, new_asset, new_log])

    # Send the blueprint.
    hostname, auth = farm_auth
    with FarmClient(hostname, auth=auth) as farm:
        post_response = farm.subrequests.send(blueprint, format=Format.json)

        # Expected results.
        response_keys = {
            "create-plant-type": {
                "attributes": {"name": "New plant type"},
                "relationships": {},
            },
            "create-asset#body{0}": {
                "attributes": {
                    "name": "My new plant",
                },
                "relationships": {
                    "plant_type": [
                        {
                            "type": "taxonomy_term--plant_type",
                            "id": "{{create-plant-type.body@$.data.id}}",
                        }
                    ]
                },
            },
            "create-log#body{0}": {
                "attributes": {
                    "name": "Seeding my new plant",
                },
                "relationships": {
                    "asset": [
                        {
                            "type": "asset--plant",
                            "id": "{{create-asset.body@$.data.id}}",
                        }
                    ]
                },
            },
        }
        for response_key, expected_data in response_keys.items():
            # Test that each response succeeded.
            assert response_key in post_response
            assert "headers" in post_response[response_key]
            assert 201 == int(post_response[response_key]["headers"]["status"][0])

            # Test that each resource was created.
            assert "body" in post_response[response_key]
            body = json.loads(post_response[response_key]["body"])
            resource_id = body["data"]["id"]
            entity_type, bundle = body["data"]["type"].split("--")
            created_resource = farm.resource.get_id(entity_type, bundle, resource_id)

            assert created_resource is not None
            assert created_resource["data"]["id"] == resource_id

            # Test for correct attributes.
            for key, value in expected_data["attributes"].items():
                assert created_resource["data"]["attributes"][key] == value

            # Test for correct relationships.
            for field_name, relationships in expected_data["relationships"].items():
                relationship_field = created_resource["data"]["relationships"][
                    field_name
                ]
                assert len(relationship_field["data"]) == len(relationships)
                for resource in relationships:
                    assert relationship_field["data"][0]["type"] == resource["type"]
