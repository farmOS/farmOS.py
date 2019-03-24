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

    })

    assert len(harvests) > 0
    assert harvests[0]['type'] == 'farm_harvest'

def test_get_farm_areas(test_farm):
    """ Test pulling area taxonomies from the server """
    areas = test_farm.areas.get()

    assert len(areas) > 0
