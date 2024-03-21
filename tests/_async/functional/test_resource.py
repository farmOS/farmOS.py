import pytest
from httpx_auth import OAuth2

from farmOS import AsyncFarmClient
from tests.conftest import farmOS_testing_server

# todo: Expand these tests to include a CRUD. Currently limited by user permissions.


@pytest.mark.anyio
@farmOS_testing_server
async def test_user_update_self(farm_auth):
    hostname, auth = farm_auth
    async with AsyncFarmClient(hostname, auth=auth) as farm:
        # Get current user ID.
        info_response = await farm.info()
        user_id = info_response["meta"]["links"]["me"]["meta"]["id"]

        user_changes = {
            "id": user_id,
            "attributes": {"timezone": "UTC"},
        }
        # Update the user.
        patch_response = await farm.resource.send("user", payload=user_changes)

        # Re-authorize the user after changing their profile.
        state, token, expires_in, refresh = farm.auth.request_new_token()
        OAuth2.token_cache._add_access_token(state, token, expires_in)

        # Get the user by ID.
        get_response = await farm.resource.get_id("user", resource_id=user_id)

        # Assert that both responses have the updated display_name.
        for response in [patch_response, get_response]:
            assert (
                response["data"]["attributes"]["timezone"]
                == user_changes["attributes"]["timezone"]
            )


@pytest.mark.anyio
@farmOS_testing_server
async def test_user_iterate(farm_auth):
    hostname, auth = farm_auth
    async with AsyncFarmClient(hostname, auth=auth) as farm:
        all_users = [
            user
            async for user in farm.resource.iterate("user", params={"page[limit]": 1})
        ]
        assert len(all_users) > 1
