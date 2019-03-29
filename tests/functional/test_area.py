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
