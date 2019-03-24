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

def test_get_records_logs(test_farm):
    """ Test pulling logs from the server """
    logs = test_farm.logs.get()
#
# Test farm info method
#

def test_get_farm_info(test_farm):
    info = test_farm.info()

    assert 'name' in info
    assert 'url' in info
    assert 'api_version' in info
    assert 'user' in info


    assert len(logs) > 0

def test_get_records_log_harvests(test_farm):
    """ Test pulling logs with 'type=farm_harvest' filter """
    harvests = test_farm.logs.get({
        'type':'farm_harvest'
    })

    assert len(harvests) > 0
    assert harvests[0]['type'] == 'farm_harvest'

def test_get_farm_areas(test_farm):
    """ Test pulling area taxonomies from the server """
    areas = test_farm.areas.get()

    assert len(areas) > 0
