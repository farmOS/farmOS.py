import farmOS

from .test_credentials import valid_credentials

def test_invalid_login():
    farm = farmOS.farmOS('test.farmos.net', 'username', 'password')
    success = farm.authenticate()

    assert success is False

def test_valid_login():
    farm = farmOS.farmOS(**valid_credentials)
    success = farm.authenticate()

    assert success is True

def test_record_request_logs():
    """ Test pulling logs from the server """
    farm = farmOS.farmOS(**valid_credentials)
    farm.authenticate()
    logs = farm.get_records('log')

    assert len(logs) > 0

def test_record_request_log_harvests():
    """ Test pulling logs with 'type=farm_harvest' filter """
    farm = farmOS.farmOS(**valid_credentials)
    farm.authenticate()
    harvests = farm.get_records('log', filters={'type':'farm_harvest'})

    assert len(harvests) > 0
    assert harvests[0]['type'] == 'farm_harvest'
