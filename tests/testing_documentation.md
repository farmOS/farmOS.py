
# farmOS Client API Testing

## Unit Tests

## Functional Tests

Functional tests require a live instance of farmOS to communicate with.
Configure credentials for the farmOS instance to test against within the `tests/test_credentials.py` file
### Authentication
These tests should live in `tests/functional/test_auth.xx`

#### `test_invalid_login`
Create an **invalid** farmOS instance and assert `farm.authenticate()` returns `False`

#### `test_valid_login`
Create an **valid** farmOS instance and assert `farm.authenticate()` returns `True`

#### `test_invalid_login`
Create a farmOS instance, call `farm.info()` before authenticating and assert a `NotAuthenticatedError` exception is raised

### Info
These tests should live in `tests/functional/test_info.xx`
All tests require an *authenticated* farmOS instance

#### `test_get_farm_info`
Save the `farm.info()` response object. Assert the keys `'name'`, `url'`, `'api_version'` and `'user'` are in the response object.

### Logs
These tests should live in `tests/functional/test_log.xx`
All tests require an *authenticated* farmOS instance

Define a test log object to be used throughout the log tests
```python
test_log = {
    'name':'Testing from farmOS.py',
    'type':'farm_observation',
}
```

#### `test_create_log`
Create the test_log with `farm.log.send(test_log)` and assert the key `'id'` is in the response object
Be sure up update the `test_log` object to include the `'id'` returned from the server so the created log can be referenced in later tests:
```python
test_log['id'] = response['id']
```

#### `test_get_all_logs`
Call `farm.log.get()` to retrieve all logs.
Assert the length of the response is `> 0`

#### `test_get_logs_filtered_by_type`
Call `farm.log.get({'type':'farm_observation'})` to retrieve observation logs.
Assert the length of the response is `> 0`

#### `test_get_log_by_id`
Using the `id` of the `test_log`, call `farm.log.get(test_log['id'])`
Assert the log returned has an `'id'` and the `'name'` matches `test_log['name']`

#### `test_update_log`
Define an object containing the log `id` and `name` attribute to change
```python
test_log_changes = {
    'id':test_log['id'],
    'name':"Updated Log Name",
}
```
Call `farm.log.send(test_log_changes)` to update the log name.
Call `farm.log.get(test_log['id'])` to retrieve the updated log and assert log has the updated `name`

#### test_delete_log
Call `farm.log.delete(test_log['id'])`
Assert the `response.status_code == 200`

### Assets
These tests should live in `tests/functional/test_asset.xx`
All tests require an *authenticated* farmOS instance

These tests are similar to those for **Logs** (see above)
#### `test_create_asset`
#### `test_get_all_assets`
#### `test_get_assets_filtered_by_type`
#### `test_get_asset_by_id`
#### `test_update_asset`
#### `test_delete_asset`

### Areas
These tests should live in `tests/functional/test_area.xx`
All tests require an *authenticated* farmOS instance

#### `test_create_area`
#### `test_get_all_farm_areas`
#### `test_get_farm_areas_filtered_by_type`
#### `test_get_farm_areas_by_id`
#### `test_update_asset`
#### `test_delete_asset`

### Terms
These tests should live in `tests/functional/test_area.xx`
All tests require an *authenticated* farmOS instance

Define a `test_term` object to used throughout the term tests:
 **NOTE** - use a helper function to search the vocabularies from `farm.term.vocabularies()` to get the VID of `farm_crops`
```python
test_term = {
    'name':'API Test Crop',
    'vocabulary': {
        'id': 3, # do not hard code this VID
        'resource':'taxonomy_vocabulary'
    }
}
```


#### `test_get_all_taxonomy_vocabularies`
Call` farm.term.vocabularies()` and assert `length`  `> 0`

#### `test_create_taxonomy_term`
#### `test_get_all_taxonomy_terms`
#### `test_get_farm_terms_filtered_by_single_vocabulary_tid`
Call `farm.term.get('farm_crops')` to get terms of the `farm_crops` vocabulary.

#### `test_farm_term_filtered_by_vocabulary_and_term_name`
Call `farm.term.get({'bundle':'farm_crops', 'name':'API Test Crop'})` to get the "API Test Crop" term

#### `test_update_taxonomy_term`
#### `test_delete_taxonomy_term`
