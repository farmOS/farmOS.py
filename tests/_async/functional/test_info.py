import pytest

from farmOS import AsyncFarmClient
from tests.conftest import farmOS_testing_server


@pytest.mark.anyio
@farmOS_testing_server
async def test_get_farm_info(farm_auth):
    hostname, auth = farm_auth
    async with AsyncFarmClient(hostname, auth=auth) as farm:
        info = await farm.info()

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
