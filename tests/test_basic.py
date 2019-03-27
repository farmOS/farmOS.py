import farmOS

from .test_credentials import valid_credentials

# Test authentication

def test_invalid_login():
    farm = farmOS.farmOS('test.farmos.net', 'username', 'password')
    success = farm.authenticate()

    assert success is False

def test_valid_login():
    farm = farmOS.farmOS(**valid_credentials)
    success = farm.authenticate()

    assert success is True

#
# Test farm info method
#

def test_get_farm_info(test_farm):
    info = test_farm.info()

    assert 'name' in info
    assert 'url' in info
    assert 'api_version' in info
    assert 'user' in info

#
# Test farm log methods
#

def test_get_all_logs(test_farm):
    logs = test_farm.log.get()

    assert len(logs) > 0

def test_get_logs_filtered_by_type(test_farm):
    log_type = 'farm_harvest'

    logs = test_farm.log.get({
        'type':log_type
    })

    assert len(logs) > 0
    assert logs[0]['type'] == log_type

def test_get_log_by_id(test_farm):
    log_id = 164
    log = test_farm.log.get(log_id)

    assert 'id' in log
    assert int(log['id']) == log_id

#
# Test farm asset methods
#

def test_get_all_assets(test_farm):
    assets = test_farm.asset.get()

    assert len(assets) > 0

def test_get_assets_filtered_by_type(test_farm):
    asset_type = 'animal'

    asset = test_farm.asset.get({
        'type':asset_type
    })

    assert len(asset) > 0
    assert asset[0]['type'] == asset_type

def test_get_asset_by_id(test_farm):
    asset_id = 1
    asset = test_farm.asset.get(asset_id)

    assert 'id' in asset
    assert int(asset['id']) == asset_id

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

#
# Test farm taxonomy term methods
#

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
    term_name = 'Spinach'

    term = test_farm.term.get({
        'bundle':vocabulary_name,
        'name':term_name
    })

    assert 'name' in term[0]
    assert term[0]['name'] == term_name
