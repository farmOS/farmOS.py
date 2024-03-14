from farmOS import FarmClient
from tests.conftest import farmOS_testing_server

# Create a test asset
test_asset = {
    "type": "equipment",
    "payload": {
        "attributes": {
            "name": "Tractor",
            "manufacturer": "Allis-Chalmers",
            "model": "G",
            "serial_number": "1234567890",
        }
    },
}


@farmOS_testing_server
def test_asset_crud(farm_auth):
    hostname, auth = farm_auth
    with FarmClient(hostname, auth=auth) as farm:
        post_response = farm.asset.send(test_asset["type"], test_asset["payload"])
        assert "id" in post_response["data"]

        # Once created, add 'id' to test_asset
        test_asset["id"] = post_response["data"]["id"]

        # Get the asset by ID.
        get_response = farm.asset.get_id(test_asset["type"], test_asset["id"])

        # Assert that both responses have the correct values.
        for response in [post_response, get_response]:
            for key, value in test_asset["payload"]["attributes"].items():
                assert response["data"]["attributes"][key] == value

        test_asset_changes = {
            "id": test_asset["id"],
            "attributes": {
                "name": "Old tractor",
                "status": "archived",
            },
        }

        # Update the asset.
        patch_response = farm.asset.send(test_asset["type"], test_asset_changes)
        # Get the asset by ID.
        get_response = farm.asset.get_id(test_asset["type"], test_asset["id"])

        # Assert that both responses have the correct values.
        for response in [patch_response, get_response]:
            for key, value in test_asset_changes["attributes"].items():
                assert response["data"]["attributes"][key] == value

        # Delete the asset.
        deleted_response = farm.asset.delete(test_asset["type"], test_asset["id"])
        assert deleted_response.status_code == 204


@farmOS_testing_server
def test_asset_get(farm_auth, test_assets):
    hostname, auth = farm_auth
    with FarmClient(hostname, auth=auth) as farm:
        # Get one page of assets.
        response = farm.asset.get(test_asset["type"])
        assert "data" in response
        assert "links" in response
        assert len(response["data"]) == 50

        # Get all assets.
        all_assets = [asset for asset in farm.asset.iterate(test_asset["type"])]
        assert len(all_assets) > len(response["data"])
