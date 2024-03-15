import os

import pytest
from httpx_auth import OAuth2ResourceOwnerPasswordCredentials

from farmOS import FarmClient

# Allow testing via http.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

FARMOS_HOSTNAME = os.getenv("FARMOS_HOSTNAME")

# Credentials for OAuth Auth
FARMOS_OAUTH_USERNAME = os.getenv("FARMOS_OAUTH_USERNAME")
FARMOS_OAUTH_PASSWORD = os.getenv("FARMOS_OAUTH_PASSWORD")
FARMOS_OAUTH_CLIENT_ID = os.getenv("FARMOS_OAUTH_CLIENT_ID", "farm")
FARMOS_OAUTH_CLIENT_SECRET = os.getenv("FARMOS_OAUTH_CLIENT_SECRET", None)

valid_oauth_config = (
    FARMOS_HOSTNAME is not None
    and FARMOS_OAUTH_USERNAME is not None
    and FARMOS_OAUTH_PASSWORD is not None
)

farmOS_testing_server = pytest.mark.skipif(
    not valid_oauth_config,
    reason="farmOS Testing Server not configured. Skipping farmOS test server integration tests.",
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="module")
def farm_auth():
    if valid_oauth_config:
        auth = OAuth2ResourceOwnerPasswordCredentials(
            token_url=f"{FARMOS_HOSTNAME}/oauth/token",
            username=FARMOS_OAUTH_USERNAME,
            password=FARMOS_OAUTH_PASSWORD,
            client_id=FARMOS_OAUTH_CLIENT_ID,
            client_secret=FARMOS_OAUTH_CLIENT_SECRET,
            scope="farm_manager",
        )
        return FARMOS_HOSTNAME, auth


@pytest.fixture(scope="module")
def test_logs(farm_auth):
    hostname, auth = farm_auth
    with FarmClient(hostname, auth=auth) as farm:
        log_ids = []
        # Create logs.
        for x in range(1, 60):
            test_log = {
                "type": "observation",
                "payload": {"attributes": {"name": "Log #" + str(x)}},
            }
            response = farm.log.send(test_log["type"], test_log["payload"])
            log_ids.append(response["data"]["id"])

        return log_ids


@pytest.fixture(scope="module")
def test_assets(farm_auth):
    hostname, auth = farm_auth
    with FarmClient(hostname, auth=auth) as farm:
        asset_ids = []
        # Create assets.
        for x in range(1, 60):
            test_asset = {
                "type": "equipment",
                "payload": {"attributes": {"name": "Asset #" + str(x)}},
            }
            response = farm.asset.send(test_asset["type"], test_asset["payload"])
            asset_ids.append(response["data"]["id"])

        return asset_ids


@pytest.fixture(scope="module")
def test_terms(farm_auth):
    hostname, auth = farm_auth
    with FarmClient(hostname, auth=auth) as farm:
        term_ids = []
        # Create terms.
        for x in range(1, 60):
            test_term = {
                "type": "plant_type",
                "payload": {"attributes": {"name": "Plant type #" + str(x)}},
            }
            response = farm.term.send(test_term["type"], test_term["payload"])
            term_ids.append(response["data"]["id"])

        return term_ids
