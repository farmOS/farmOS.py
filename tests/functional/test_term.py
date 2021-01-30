from tests.conftest import farmOS_testing_server

test_term = {
    "type": "plant_type",
    "payload": {"attributes": {"name": "Corn"}},
}


@farmOS_testing_server
def test_term_crud(test_farm):
    post_response = test_farm.term.send(test_term["type"], test_term["payload"])
    assert "id" in post_response["data"]

    # Once created, add 'id' to test_term
    test_term["id"] = post_response["data"]["id"]

    # Get the term by ID.
    get_response = test_farm.term.get_id(test_term["type"], test_term["id"])

    # Assert that both responses have the correct values.
    for response in [post_response, get_response]:
        for key, value in test_term["payload"]["attributes"].items():
            assert response["data"]["attributes"][key] == value

    test_term_changes = {
        "id": test_term["id"],
        "attributes": {"name": "Updated corn"},
    }
    # Update the term.
    patch_response = test_farm.term.send(test_term["type"], test_term_changes)
    # Get the term by ID.
    get_response = test_farm.term.get_id(test_term["type"], test_term["id"])

    # Assert that both responses have the updated name.
    for response in [patch_response, get_response]:
        assert (
            response["data"]["attributes"]["name"]
            == test_term_changes["attributes"]["name"]
        )

    # Delete the term.
    deleted_response = test_farm.term.delete(test_term["type"], test_term["id"])
    assert deleted_response.status_code == 204


@farmOS_testing_server
def test_term_get(test_farm, test_terms):
    # Get one page of plant_type terms.
    response = test_farm.term.get(test_term["type"])
    assert "data" in response
    assert "links" in response
    assert len(response["data"]) == 50

    # Get all plant_type terms.
    all_terms = list(test_farm.term.iterate(test_term["type"]))
    assert len(all_terms) > len(response["data"])
