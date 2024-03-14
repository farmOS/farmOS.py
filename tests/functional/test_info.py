from farmOS import FarmClient
from tests.conftest import farmOS_testing_server


#
# Test farm info method
#
@farmOS_testing_server
def test_get_farm_info(farm_auth):
    hostname, auth = farm_auth
    with FarmClient(hostname, auth=auth) as farm:
        info = farm.info()

        assert "links" in info
        assert "meta" in info

        # Test user links info.
        assert "links" in info["meta"]
        assert "me" in info["meta"]["links"]

        # Test farm info.
        assert "farm" in info["meta"]
        farm_info = info["meta"]["farm"]
        assert "name" in farm_info
        assert "url" in farm_info
        assert "version" in farm_info
