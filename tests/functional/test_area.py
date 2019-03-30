def _search_for_vocab_id(name, vocabs):
    return [vocab for vocab in vocabs if vocab['machine_name'] == name]

test_area = {
    'name':'Testing area',
    'area_type':'field',
    'vocabulary': {
        'id':None,
        'resource':'taxonomy_vocabulary'
    }
}

#
# Test farm area methods
#

def test_get_all_farm_areas(test_farm):
    areas = test_farm.area.get()

    assert len(areas) > 0

def test_get_farm_areas_filtered_by_type(test_farm):
    area_type = 'field'

    areas = test_farm.area.get({
        'area_type':area_type
    })

    assert len(areas) > 0
    assert areas[0]['area_type'] == area_type

def test_get_farm_areas_by_id(test_farm):
    area_tid = 5
    areas = test_farm.area.get(area_tid)
    area = areas[0]

    assert 'tid' in area
    assert int(area['tid']) == area_tid

def test_create_area(test_farm):
    # Find the vocab ID for farm_areas
    vocabs = test_farm.term.vocabularies()
    farm_areas_id = _search_for_vocab_id('farm_areas', vocabs)[0]['vid']
    # Update the test_area with the vid
    test_area['vocabulary']['id'] = farm_areas_id

    response = test_farm.area.send(test_area)
    print(test_area, response)
    assert 'id' in response

    # Once created, add 'id' to test_asset
    test_area['id'] = response['id']

def test_delete_area(test_farm):
    response = test_farm.area.delete(int(test_area['id']))
    assert response.status_code == 200
