import pytest
import os

from requests import HTTPError
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
from oauthlib.oauth2 import (
    InvalidClientError,
    InvalidScopeError,
)
from farmOS import farmOS

from tests.conftest import farmOS_testing_server

# Variables for testing.
FARMOS_HOSTNAME = os.getenv("FARMOS_HOSTNAME")
FARMOS_OAUTH_USERNAME = os.getenv("FARMOS_OAUTH_USERNAME")
FARMOS_OAUTH_PASSWORD = os.getenv("FARMOS_OAUTH_PASSWORD")


@farmOS_testing_server
def test_invalid_login():
    # todo: simple_oauth returns invalid_credentials instead of invalid_grant.
    # https://www.drupal.org/project/simple_oauth/issues/3193609
    with pytest.raises(CustomOAuth2Error, match=r"invalid_credentials *."):
        farm = farmOS(hostname=FARMOS_HOSTNAME, scope="farm_manager", version=2)
        farm.authorize("username", "password")


@farmOS_testing_server
def test_invalid_client_id():
    with pytest.raises(InvalidClientError):
        farm = farmOS(
            hostname=FARMOS_HOSTNAME,
            scope="farm_manager",
            client_id="bad_client",
            version=2,
        )
        farm.authorize(FARMOS_OAUTH_USERNAME, FARMOS_OAUTH_PASSWORD)


@farmOS_testing_server
@pytest.mark.skip(
    reason="simple_oauth seems to accept any secret if none is configured on the client."
)
def test_invalid_client_secret():
    with pytest.raises(InvalidClientError):
        farm = farmOS(FARMOS_HOSTNAME, client_id="farm", client_secret="bad_pass")
        farm.authorize(FARMOS_OAUTH_USERNAME, FARMOS_OAUTH_PASSWORD)


@farmOS_testing_server
def test_invalid_scope():
    with pytest.raises(InvalidScopeError):
        farm = farmOS(hostname=FARMOS_HOSTNAME, scope="bad_scope", version=2)
        farm.authorize(FARMOS_OAUTH_USERNAME, FARMOS_OAUTH_PASSWORD, scope="bad_scope")


@farmOS_testing_server
@pytest.mark.skip(reason="JSONAPI endpoints don't return 403.")
def test_unauthorized_request(test_farm):
    with pytest.raises(HTTPError, match=r"403 *."):
        farm = farmOS(hostname=FARMOS_HOSTNAME, scope="farm_manager", version=2)
        farm.log.get("activity")


@farmOS_testing_server
def test_valid_login(test_farm):
    token = test_farm.authorize(
        username=FARMOS_OAUTH_USERNAME, password=FARMOS_OAUTH_PASSWORD
    )

    assert "access_token" in token
    assert "refresh_token" in token
