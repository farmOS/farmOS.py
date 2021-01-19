from tests.conftest import farmOS_testing_server

#
# Test farm info method
#
@farmOS_testing_server
def test_get_farm_info(test_farm):
    info = test_farm.info()

    assert "links" in info
    assert "meta" in info

    # Test farm info.
    assert "farm" in info["meta"]
    farm_info = info["meta"]["farm"]
    assert "name" in farm_info
    assert "url" in farm_info
    assert "version" in farm_info
