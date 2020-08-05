import pytest
import os

import farmOS
from oauthlib.oauth2 import InvalidGrantError

from tests.conftest import farmOS_testing_server


# Test authentication
@farmOS_testing_server
def test_invalid_login():
    with pytest.raises(InvalidGrantError):
        farm = farmOS.farmOS('test.farmos.net')
        farm.authorize('username', 'password')


@farmOS_testing_server
def test_valid_login(test_farm):
    FARMOS_OAUTH_USERNAME = os.getenv("FARMOS_OAUTH_USERNAME")
    FARMOS_OAUTH_PASSWORD = os.getenv("FARMOS_OAUTH_PASSWORD")
    token = test_farm.authorize(username=FARMOS_OAUTH_USERNAME, password=FARMOS_OAUTH_PASSWORD)

    assert 'access_token' in token
    assert 'refresh_token' in token
