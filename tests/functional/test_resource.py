import os

from tests.conftest import farmOS_testing_server

FARMOS_OAUTH_USERNAME = os.getenv("FARMOS_OAUTH_USERNAME")
FARMOS_OAUTH_PASSWORD = os.getenv("FARMOS_OAUTH_PASSWORD")

# todo: Expand these tests to include a CRUD. Currently limited by user permissions.


@farmOS_testing_server
def test_user_update_self(test_farm):
    # Get current user ID.
    info_response = test_farm.info()
    user_id = info_response["meta"]["links"]["me"]["meta"]["id"]

    user_changes = {
        "id": user_id,
        "attributes": {"timezone": "UTC"},
    }
    # Update the user.
    patch_response = test_farm.resource.send("user", payload=user_changes)

    # Re-authorize the user after changing their profile.
    test_farm.authorize(username=FARMOS_OAUTH_USERNAME, password=FARMOS_OAUTH_PASSWORD)

    # Get the user by ID.
    get_response = test_farm.resource.get_id("user", resource_id=user_id)

    # Assert that both responses have the updated display_name.
    for response in [patch_response, get_response]:
        assert (
            response["data"]["attributes"]["timezone"]
            == user_changes["attributes"]["timezone"]
        )


@farmOS_testing_server
def test_user_iterate(test_farm):
    all_users = list(test_farm.resource.iterate("user", params={"page[limit]": 1}))

    assert len(all_users) > 1
