import pytest
import os

import farmOS

FARMOS_HOSTNAME = os.getenv("FARMOS_HOSTNAME")

# Credentials for Drupal RestWS Auth
FARMOS_RESTWS_USERNAME = os.getenv("FARMOS_RESTWS_USERNAME")
FARMOS_RESTWS_PASSWORD = os.getenv("FARMOS_RESTWS_PASSWORD")

# Credentials for OAuth Auth
FARMOS_OAUTH_USERNAME = os.getenv("FARMOS_OAUTH_USERNAME")
FARMOS_OAUTH_PASSWORD = os.getenv("FARMOS_OAUTH_PASSWORD")
FARMOS_OAUTH_CLIENT_ID = os.getenv("FARMOS_OAUTH_CLIENT_ID")
FARMOS_OAUTH_CLIENT_SECRET = os.getenv("FARMOS_OAUTH_CLIENT_SECRET")

valid_restws_config = \
    FARMOS_HOSTNAME is not None and FARMOS_RESTWS_USERNAME is not None and FARMOS_RESTWS_PASSWORD is not None

valid_oauth_config = \
    FARMOS_HOSTNAME is not None and FARMOS_OAUTH_USERNAME is not None and FARMOS_OAUTH_PASSWORD is not None \
    and FARMOS_OAUTH_CLIENT_ID is not None and FARMOS_OAUTH_CLIENT_SECRET is not None

farmOS_testing_server = pytest.mark.skipif(
    not (valid_restws_config or valid_oauth_config),
    reason="farmOS Testing Server not configured. Skipping farmOS test server integration tests.",
)

@pytest.fixture(scope='module')
def test_farm():
    if valid_restws_config:
        farm = farmOS.farmOS(FARMOS_HOSTNAME, FARMOS_RESTWS_USERNAME, FARMOS_RESTWS_PASSWORD)
        farm.authenticate()
        return farm

    if valid_oauth_config:
        farm = farmOS.farmOS(FARMOS_HOSTNAME, username=FARMOS_OAUTH_USERNAME, password=FARMOS_OAUTH_PASSWORD,
                             client_id=FARMOS_OAUTH_CLIENT_ID, client_secret=FARMOS_OAUTH_CLIENT_SECRET)
        farm.authenticate()
        return farm
