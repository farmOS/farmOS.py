import pytest
import os

from farmOS import (
    farmOS,
    HTTPError,
    InvalidGrantError,
    InvalidClientError,
    InvalidScopeError,
)

from tests.conftest import farmOS_testing_server

# Variables for testing.
FARMOS_HOSTNAME = os.getenv("FARMOS_HOSTNAME")
FARMOS_OAUTH_USERNAME = os.getenv("FARMOS_OAUTH_USERNAME")
FARMOS_OAUTH_PASSWORD = os.getenv("FARMOS_OAUTH_PASSWORD")


@farmOS_testing_server
def test_invalid_login():
    with pytest.raises(InvalidGrantError):
        farm = farmOS(FARMOS_HOSTNAME)
        farm.authorize("username", "password")


@farmOS_testing_server
def test_invalid_client_id():
    with pytest.raises(InvalidClientError):
        farm = farmOS(FARMOS_HOSTNAME, client_id="bad_client")
        farm.authorize(FARMOS_OAUTH_USERNAME, FARMOS_OAUTH_PASSWORD)


@farmOS_testing_server
def test_invalid_client_secret():
    with pytest.raises(InvalidClientError):
        farm = farmOS(FARMOS_HOSTNAME, client_id="farm", client_secret="bad_pass")
        farm.authorize(FARMOS_OAUTH_USERNAME, FARMOS_OAUTH_PASSWORD)


@farmOS_testing_server
def test_invalid_scopet():
    with pytest.raises(InvalidScopeError):
        farm = farmOS(FARMOS_HOSTNAME, scope="bad_scope")
        farm.authorize(FARMOS_OAUTH_USERNAME, FARMOS_OAUTH_PASSWORD, scope="bad_scope")


@farmOS_testing_server
def test_unauthorized_request(test_farm):
    with pytest.raises(HTTPError, match=r"403 *."):
        farm = farmOS(FARMOS_HOSTNAME)
        farm.log.get()


@farmOS_testing_server
def test_valid_login(test_farm):
    token = test_farm.authorize(
        username=FARMOS_OAUTH_USERNAME, password=FARMOS_OAUTH_PASSWORD
    )

    assert "access_token" in token
    assert "refresh_token" in token
