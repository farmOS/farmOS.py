import pytest

import farmOS

from tests.conftest import farmOS_testing_server
from farmOS.exceptions import NotAuthenticatedError

# Test authentication

@farmOS_testing_server
def test_invalid_login():
    farm = farmOS.farmOS('test.farmos.net', 'username', 'password')
    success = farm.authenticate()

    assert success is False


@farmOS_testing_server
def test_valid_login(test_farm):
    success = test_farm.authenticate()

    assert success is True


@farmOS_testing_server
def test_not_authenticated_exception_raised():
    with pytest.raises(NotAuthenticatedError):
        farm = farmOS.farmOS('test.farmos.net', 'username', 'password')
        farm.info()
