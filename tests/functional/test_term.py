from tests.conftest import farmOS_testing_server

test_term = {
    "name": "API Test Crop",
    "vocabulary": {"id": None, "resource": "taxonomy_vocabulary"},
}

#
# Test farm taxonomy term methods
#
@farmOS_testing_server
def test_create_taxonomy_term(test_farm):
    # Find the vocab ID for farm_crops
    content = test_farm.info()

    # Check that farm info includes farm_crops vid
    assert "resources" in content
    assert "taxonomy_term" in content["resources"]
    assert "farm_crops" in content["resources"]["taxonomy_term"]
    assert "vid" in content["resources"]["taxonomy_term"]["farm_crops"]

    farm_crop_id = content["resources"]["taxonomy_term"]["farm_crops"]["vid"]

    # Update the test_term with the vid
    test_term["vocabulary"]["id"] = farm_crop_id

    response = test_farm.term.send(test_term)
    assert "id" in response

    # Once created, add 'id' to test_asset
    test_term["id"] = response["id"]


@farmOS_testing_server
def test_get_all_taxonomy_terms(test_farm):
    terms = test_farm.term.get()

    assert "list" in terms
    assert "page" in terms
    assert len(terms) > 0


@farmOS_testing_server
def test_get_farm_terms_filtered_by_single_vocabulary_name(test_farm):
    vocabulary_name = "farm_crops"

    terms = test_farm.term.get(vocabulary_name)

    assert len(terms) > 0
    # Assert all terms retrieved are from the same vocabulary
    # (cannot check vocabulary name in response)
    assert terms["list"][0]["vocabulary"]["id"] == terms["list"][1]["vocabulary"]["id"]


@farmOS_testing_server
def test_get_farm_terms_filtered_by_single_vocabulary_tid(test_farm):
    vocabulary_tid = 7

    term = test_farm.term.get(vocabulary_tid)

    assert "vocabulary" in term
    assert int(term["tid"]) == vocabulary_tid


@farmOS_testing_server
def test_get_farm_term_filtered_by_multiple_vocabulary(test_farm):
    vocabulary_name = "farm_crops"
    term_name = "API Test Crop"

    term = test_farm.term.get({"bundle": vocabulary_name, "name": term_name})

    assert "name" in term["list"][0]
    assert term["list"][0]["name"] == term_name


@farmOS_testing_server
def test_update_taxonomy_term(test_farm):
    test_term_changes = {"id": test_term["id"], "name": "Crop changed name"}
    response = test_farm.term.send(test_term_changes)
    assert "id" in response
    assert response["id"] == test_term["id"]

    updated_term = test_farm.term.get(int(test_term["id"]))
    assert updated_term["name"] == test_term_changes["name"]


@farmOS_testing_server
def test_delete_taxonomy_term(test_farm):
    response = test_farm.term.delete(int(test_term["id"]))
    assert response.status_code == 200
