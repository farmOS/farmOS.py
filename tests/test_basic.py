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
    log_type = 'harvest'

    logs = test_farm.log.get({
        'type':log_type
    })

    assert len(logs) > 0
    assert logs[0]['type'] == log_type

def test_get_log_by_id(test_farm):
    log_id = 5
    log = test_farm.log.get(log_id)

    assert 'id' in log
    assert log['id'] == log_id

#
# Test farm asset methods
#

def test_get_all_assets(test_farm):
    assets = test_farm.asset.get()

    assert len(assets) > 0

def test_get_assets_filtered_by_type(test_farm):
    asset_type = 'animal'

    assets = test_farm.asset.get({
        'type':asset_type
    })

    assert len(assets) > 0
    assert asset[0]['type'] == asset_type

def test_get_asset_by_id(test_farm):
    asset_id = 5
    asset = test_farm.asset.get(asset_id)

    assert 'id' in asset
    assert asset['id'] == asset_id

#
# Test farm area methods
#

def test_get_all_farm_areas(test_farm):
    areas = test_farm.area.get()

    assert len(areas) > 0

def test_get_farm_areas_filtered_by_type(test_farm):
    area_type = 'field'

    areas = test_farm.area.get({
        'type':area_type
    })

    assert len(areas) > 0
    assert areas[0]['type'] == area_type

def test_get_farm_areas_by_id(test_farm):
    area_id = 5
    area = test_farm.area.get(area_id)

    assert 'id' in area
    assert area['id'] == area_id

