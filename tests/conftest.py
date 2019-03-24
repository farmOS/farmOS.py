import pytest

import farmOS

from .test_credentials import valid_credentials

@pytest.fixture(scope='module')
def test_farm():
    farm = farmOS.farmOS(**valid_credentials)
    farm.authenticate()
    return farm
