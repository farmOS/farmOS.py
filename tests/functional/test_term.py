test_term = {
    'name':'API Test Crop',
    'vocabulary': {
        'id':None,
        'resource':'taxonomy_vocabulary'
    }
}
#
# Test farm taxonomy term methods
#

def test_create_taxonomy_term(test_farm):
    # Find the vocab ID for farm_crops
    farm_crop_id = test_farm.vocabulary('farm_crops')[0]['vid']
    
    # Update the test_term with the vid
    test_term['vocabulary']['id'] = farm_crop_id

    response = test_farm.term.send(test_term)
    assert 'id' in response

    # Once created, add 'id' to test_asset
    test_term['id'] = response['id']

def test_get_all_taxonomy_terms(test_farm):
    terms = test_farm.term.get()

    assert len(terms) > 0

def test_get_farm_terms_filtered_by_single_vocabulary_name(test_farm):
    vocabulary_name = 'farm_crops'

    terms = test_farm.term.get(vocabulary_name)

    assert len(terms) > 0
    # Assert all terms retrieved are from the same vocabulary
    # (cannot check vocabulary name in response)
    assert terms[0]['vocabulary']['id'] == terms[1]['vocabulary']['id']

def test_get_farm_terms_filtered_by_single_vocabulary_tid(test_farm):
    vocabulary_tid = 7

    term = test_farm.term.get(vocabulary_tid)

    assert 'vocabulary' in term
    assert int(term['tid']) == vocabulary_tid

def test_get_farm_term_filtered_by_multiple_vocabulary(test_farm):
    vocabulary_name = 'farm_crops'
    term_name = 'API Test Crop'

    term = test_farm.term.get({
        'bundle':vocabulary_name,
        'name':term_name
    })

    assert 'name' in term[0]
    assert term[0]['name'] == term_name

def test_update_taxonomy_term(test_farm):
    test_term_changes = {
        'id':test_term['id'],
        'name':'Crop changed name'
    }
    test_farm.term.send(test_term_changes)

    updated_term = test_farm.term.get(int(test_term['id']))
    assert updated_term['name'] == test_term_changes['name']

def test_delete_taxonomy_term(test_farm):
    response = test_farm.term.delete(int(test_term['id']))
    assert response.status_code == 200
