from datetime import datetime, timezone

from tests.conftest import farmOS_testing_server

curr_time = datetime.now(timezone.utc)
timestamp = curr_time.isoformat(timespec="seconds")

# Create a test log
test_log = {
    "type": "observation",
    "payload": {
        "attributes": {"name": "Testing from farmOS.py", "timestamp": timestamp,},
    },
}


@farmOS_testing_server
def test_log_crud(test_farm):
    post_response = test_farm.log.send(test_log["type"], test_log["payload"])
    assert "id" in post_response["data"]

    # Once created, add 'id' to test_log
    test_log["id"] = post_response["data"]["id"]

    # Get the log by ID.
    get_response = test_farm.log.get(test_log["type"], test_log["id"])

    # Assert that both responses have the correct values.
    for response in [post_response, get_response]:
        for key, value in test_log["payload"]["attributes"].items():
            assert response["data"]["attributes"][key] == value

    test_log_changes = {
        "id": test_log["id"],
        "attributes": {"name": "Updated Log Name",},
    }
    # Update the log.
    patch_response = test_farm.log.send(test_log["type"], test_log_changes)
    # Get the log by ID.
    get_response = test_farm.log.get(test_log["type"], test_log["id"])

    # Assert that both responses have the updated name.
    for response in [patch_response, get_response]:
        assert (
            response["data"]["attributes"]["name"]
            == test_log_changes["attributes"]["name"]
        )

    # Delete the log.
    deleted_response = test_farm.log.delete(test_log["type"], test_log["id"])
    assert deleted_response.status_code == 204


@farmOS_testing_server
def test_log_get(test_farm, test_logs):
    # Get one page of logs.
    response = test_farm.log.get(test_log["type"])
    assert "data" in response
    assert "links" in response
    assert len(response["data"]) == 50

    # Get all logs.
    all_logs = list(test_farm.log.iterate(test_log["type"]))
    assert len(all_logs) > len(response["data"])
