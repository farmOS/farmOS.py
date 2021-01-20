import pytest
import os

import farmOS

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


@pytest.fixture(scope="module")
def test_farm():
    if valid_oauth_config:
        farm = farmOS.farmOS(
            hostname=FARMOS_HOSTNAME,
            scope="farm_manager",
            client_id=FARMOS_OAUTH_CLIENT_ID,
            client_secret=FARMOS_OAUTH_CLIENT_SECRET,
            version=2,
        )
        farm.authorize(username=FARMOS_OAUTH_USERNAME, password=FARMOS_OAUTH_PASSWORD)
        return farm


@pytest.fixture(scope="module")
def test_logs(test_farm):
    log_ids = []
    # Create logs.
    for x in range(1, 60):
        test_log = {
            "type": "observation",
            "payload": {"attributes": {"name": "Log #" + str(x)}},
        }
        response = test_farm.log.send(test_log["type"], test_log["payload"])
        log_ids.append(response["data"]["id"])

    return log_ids


@pytest.fixture(scope="module")
def test_assets(test_farm):
    asset_ids = []
    # Create assets.
    for x in range(1, 60):
        test_asset = {
            "type": "equipment",
            "payload": {"attributes": {"name": "Asset #" + str(x)}},
        }
        response = test_farm.asset.send(test_asset["type"], test_asset["payload"])
        asset_ids.append(response["data"]["id"])

    return asset_ids


@pytest.fixture(scope="module")
def test_terms(test_farm):
    term_ids = []
    # Create terms.
    for x in range(1, 60):
        test_term = {
            "type": "plant_type",
            "payload": {"attributes": {"name": "Plant type #" + str(x)}},
        }
        response = test_farm.term.send(test_term["type"], test_term["payload"])
        term_ids.append(response["data"]["id"])

    return term_ids
