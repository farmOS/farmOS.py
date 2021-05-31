
# farmOS Client API Testing

## Unit Tests

## Functional Tests
All functional tests require an *authenticated* farmOS instance

Configure credentials for the farmOS instance to test against by setting the following environment variables: 

For farmOS OAuth Authentication (Password Flow):
`FARMOS_HOSTNAME`, `FARMOS_OAUTH_USERNAME`, `FARMOS_OAUTH_PASSWORD`, `FARMOS_OAUTH_CLIENT_ID`, `FARMOS_OAUTH_CLIENT_SECRET`

### Authentication
These tests should live in `tests/functional/test_auth.xx`

### Info
These tests should live in `tests/functional/test_info.xx`

### Logs
These tests should live in `tests/functional/test_log.xx`

### Assets
These tests should live in `tests/functional/test_asset.xx`

### Terms
These tests should live in `tests/functional/test_terms.xx`
