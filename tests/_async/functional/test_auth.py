import os

import pytest
from httpx_auth import InvalidGrantRequest, OAuth2ResourceOwnerPasswordCredentials

from farmOS import AsyncFarmClient
from tests.conftest import farmOS_testing_server

# Variables for testing.
FARMOS_HOSTNAME = os.getenv("FARMOS_HOSTNAME")
FARMOS_OAUTH_USERNAME = os.getenv("FARMOS_OAUTH_USERNAME")
FARMOS_OAUTH_PASSWORD = os.getenv("FARMOS_OAUTH_PASSWORD")
FARMOS_OAUTH_CLIENT_ID = os.getenv("FARMOS_OAUTH_CLIENT_ID", "farm")
FARMOS_OAUTH_CLIENT_SECRET = os.getenv("FARMOS_OAUTH_CLIENT_SECRET", None)


@pytest.mark.anyio
@farmOS_testing_server
async def test_invalid_login():
    with pytest.raises(InvalidGrantRequest):
        auth = OAuth2ResourceOwnerPasswordCredentials(
            token_url=f"{FARMOS_HOSTNAME}/oauth/token",
            username="username",
            password="password",
            client_id=FARMOS_OAUTH_CLIENT_ID,
            client_secret=FARMOS_OAUTH_CLIENT_SECRET,
            scope="farm_manager",
        )
        farm = AsyncFarmClient(hostname=FARMOS_HOSTNAME, auth=auth)
        await farm.info()


@pytest.mark.anyio
@farmOS_testing_server
async def test_invalid_client_id():
    with pytest.raises(InvalidGrantRequest):
        auth = OAuth2ResourceOwnerPasswordCredentials(
            token_url=f"{FARMOS_HOSTNAME}/oauth/token",
            username=FARMOS_OAUTH_USERNAME,
            password=FARMOS_OAUTH_PASSWORD,
            client_id="bad_client",
            client_secret=FARMOS_OAUTH_CLIENT_SECRET,
            scope="farm_manager",
        )
        farm = AsyncFarmClient(hostname=FARMOS_HOSTNAME, auth=auth)
        await farm.info()


@pytest.mark.anyio
@pytest.mark.skip(
    reason="simple_oauth seems to accept any secret if none is configured on the client."
)
@farmOS_testing_server
async def test_invalid_client_secret():
    with pytest.raises(InvalidGrantRequest):
        auth = OAuth2ResourceOwnerPasswordCredentials(
            token_url=f"{FARMOS_HOSTNAME}/oauth/token",
            username=FARMOS_OAUTH_USERNAME,
            password=FARMOS_OAUTH_PASSWORD,
            client_id=FARMOS_OAUTH_CLIENT_ID,
            client_secret="bad secret",
            scope="farm_manager",
        )
        farm = AsyncFarmClient(hostname=FARMOS_HOSTNAME, auth=auth)
        await farm.info()


@pytest.mark.anyio
@farmOS_testing_server
async def test_invalid_scope():
    with pytest.raises(InvalidGrantRequest):
        auth = OAuth2ResourceOwnerPasswordCredentials(
            token_url=f"{FARMOS_HOSTNAME}/oauth/token",
            username=FARMOS_OAUTH_USERNAME,
            password=FARMOS_OAUTH_PASSWORD,
            client_id=FARMOS_OAUTH_CLIENT_ID,
            client_secret=FARMOS_OAUTH_CLIENT_SECRET,
            scope="bad_scope",
        )
        farm = AsyncFarmClient(hostname=FARMOS_HOSTNAME, auth=auth)
        await farm.info()


@pytest.mark.anyio
@farmOS_testing_server
async def test_valid_login():
    auth = OAuth2ResourceOwnerPasswordCredentials(
        token_url=f"{FARMOS_HOSTNAME}/oauth/token",
        username=FARMOS_OAUTH_USERNAME,
        password=FARMOS_OAUTH_PASSWORD,
        client_id=FARMOS_OAUTH_CLIENT_ID,
        client_secret=FARMOS_OAUTH_CLIENT_SECRET,
        scope="farm_manager",
    )
    farm = AsyncFarmClient(hostname=FARMOS_HOSTNAME, auth=auth)

    # Re-authorize the user after changing their profile.
    state, token, expires_in, refresh = farm.auth.request_new_token()
    assert ".ey" in token
    # Expiration should be 3600 but can fluctuate during tests.
    assert 3590 < expires_in < 3610
    assert refresh is not None

    # Check that the user info is provided at farm.info.
    info = await farm.info()
    assert "meta" in info
    assert "links" in info["meta"]
    assert "me" in info["meta"]["links"]
