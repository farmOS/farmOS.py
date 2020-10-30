from tests.conftest import farmOS_testing_server

#
# Test farm info method
#
@farmOS_testing_server
def test_get_farm_info(test_farm):
    info = test_farm.info()

    assert "name" in info
    assert "url" in info
    assert "api_version" in info
    assert "user" in info
    assert "resources" in info
