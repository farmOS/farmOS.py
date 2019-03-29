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
