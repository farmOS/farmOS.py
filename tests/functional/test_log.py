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
