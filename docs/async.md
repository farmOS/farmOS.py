# Async support

farmOS.py offers support for an async client if you need it. This is made
possible by the [HTTPX](https://www.python-httpx.org/) HTTP Python client that
farmOS.py uses.

The async client may be more efficient when making many requests to the farmOS
server and may be useful when working in an async Python framework.

## Making Async requests

Below are simple examples of using the async client. For more information see
the [HTTPX Async documentation](https://python-httpx.org/async/).

To make asynchronous requests, you'll need an `AsyncFarmClient`.

```python
from farmOS import AsyncFarmClient

hostname, auth = farm_auth
async with AsyncFarmClient(hostname, auth=auth) as farm:
    # Get one page of animal assets.
    response = await farm.asset.get("animal")
```

### Making requests

All of the standard client resource methods are async, so you should use
`response = await farm_client.resource.get()` style for all of the following:

- `resource.get(entity_type, bundle, params)`
- `resource.get_id(entity_type, bundle, id)`
- `resource.iterate(entity_type, bundle, params)`
- `resource.send(entity_type, bundle, payload)`
- `resource.delete(entity_type, bundle, id)`

### Opening and closing clients

Use `async with AsyncFarmClient() as client:` if you want a context-managed client:

```python
async with AsyncFarmClient() as client:
    ...
```

Alternatively, use `await farm_client.aclose()` if you want to close a client explicitly:

```python
farm_client = AsyncFarmClient()
...
await farm_client.aclose()
```

### Examples

See the following examples from the [async Asset test (test_asset.py)](../tests/_async/functional/test_asset.py):

```python
from farmOS import AsyncFarmClient

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

async def test_asset_crud(farm_auth):
    hostname, auth = farm_auth
    async with AsyncFarmClient(hostname, auth=auth) as farm:
        post_response = await farm.asset.send(test_asset["type"], test_asset["payload"])
        assert "id" in post_response["data"]

        # Once created, add 'id' to test_asset
        test_asset["id"] = post_response["data"]["id"]

        # Get the asset by ID.
        get_response = await farm.asset.get_id(test_asset["type"], test_asset["id"])

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
        patch_response = await farm.asset.send(test_asset["type"], test_asset_changes)
        # Get the asset by ID.
        get_response = await farm.asset.get_id(test_asset["type"], test_asset["id"])

        # Assert that both responses have the correct values.
        for response in [patch_response, get_response]:
            for key, value in test_asset_changes["attributes"].items():
                assert response["data"]["attributes"][key] == value

        # Delete the asset.
        deleted_response = await farm.asset.delete(test_asset["type"], test_asset["id"])
        assert deleted_response.status_code == 204


async def test_asset_get(farm_auth, test_assets):
    hostname, auth = farm_auth
    async with AsyncFarmClient(hostname, auth=auth) as farm:
        # Get one page of assets.
        response = await farm.asset.get(test_asset["type"])
        assert "data" in response
        assert "links" in response
        assert len(response["data"]) == 50

        # Get all assets.
        all_assets = [asset async for asset in farm.asset.iterate(test_asset["type"])]
        assert len(all_assets) > len(response["data"])
```