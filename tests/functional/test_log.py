from datetime import datetime

from tests.conftest import farmOS_testing_server

curr_time = datetime.now()
timestamp = datetime.timestamp(curr_time)
timestamp = str(timestamp)[0:-7]

# Create a test log
test_log = {
    'name':'Testing from farmOS.py',
    'type':'farm_observation',
    'timestamp':timestamp
}

#
# Test farm log methods
#
@farmOS_testing_server
def test_create_log(test_farm):
    response = test_farm.log.send(test_log)
    assert 'id' in response

    # Once created, add 'id' to test_log
    test_log['id'] = response['id']

    created_log = test_farm.log.get(response['id'])
    assert created_log['timestamp'] == test_log['timestamp']


@farmOS_testing_server
def test_get_one_page_of_logs(test_farm):
    logs = test_farm.log.get({'page':0})

    assert 'list' in logs
    assert 'page' in logs
    assert len(logs['list']) > 0
    assert logs['page']['self'] == 0


@farmOS_testing_server
def test_get_all_logs(test_farm):
    one_page_logs = test_farm.log.get({'page':0})
    all_logs = test_farm.log.get()

    assert 'page' in all_logs
    assert all_logs['page']['last'] != all_logs['page']['first']
    assert len(all_logs['list']) > len(one_page_logs['list'])


@farmOS_testing_server
def test_get_logs_filtered_by_type(test_farm):
    log_type = test_log['type']

    logs = test_farm.log.get({
        'type':log_type
    })

    assert len(logs) > 0
    assert logs['list'][0]['type'] == log_type


@farmOS_testing_server
def test_get_log_by_id(test_farm):
    log_id = test_log['id']
    log = test_farm.log.get(log_id)

    assert 'id' in log
    assert log['id'] == log_id


@farmOS_testing_server
def test_update_log(test_farm):
    test_log_changes = {
        'id':test_log['id'],
        'name':"Updated Log Name",
    }
    response = test_farm.log.send(test_log_changes)
    assert 'id' in response
    assert response['id'] == test_log['id']

    updated_log = test_farm.log.get(test_log['id'])
    assert updated_log['name'] == test_log_changes['name']


@farmOS_testing_server
def test_delete_log(test_farm):
    deleted_response = test_farm.log.delete(test_log['id'])
    assert deleted_response.status_code == 200
