# Create a test asset
test_asset = {
  "name": "Tractor",
  "type": "equipment",
  "manufacturer": "Allis-Chambers",
  "model": "G",
  "serial_number": "1234567890",
}

#
# Test farm asset methods
#
def test_create_asset(test_farm):
    response = test_farm.asset.send(test_asset)

    assert 'id' in response

    # Once created, add 'id' to test_asset
    test_asset['id'] = response['id']

def test_get_all_assets(test_farm):
    assets = test_farm.asset.get()

    assert len(assets) > 0

def test_get_assets_filtered_by_type(test_farm):
    asset_type = test_asset['type']

    asset = test_farm.asset.get({
        'type':asset_type
    })

    assert len(asset) > 0
    assert asset[0]['type'] == asset_type

def test_get_asset_by_id(test_farm):
    asset_id = test_asset['id']
    asset = test_farm.asset.get(asset_id)

    assert 'id' in asset
    assert asset['id'] == asset_id

def test_update_asset(test_farm):
    test_asset_changes = {
        'id':test_asset['id'],
        'serial_number':'0123456789'
    }
    response = test_farm.asset.send(test_asset_changes)
    assert 'id' in response
    assert response['id'] == test_asset['id']

    updated_asset = test_farm.asset.get(test_asset['id'])

    assert updated_asset['serial_number'] == test_asset_changes['serial_number']

def test_delete_asset(test_farm):
    response = test_farm.asset.delete(test_asset['id'])

    assert response.status_code == 200
