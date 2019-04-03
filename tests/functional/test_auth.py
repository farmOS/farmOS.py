import pytest

import farmOS

from tests.test_credentials import valid_credentials
from farmOS.exceptions import NotAuthenticatedError

# Test authentication

def test_invalid_login():
    farm = farmOS.farmOS('test.farmos.net', 'username', 'password')
    success = farm.authenticate()

    assert success is False

def test_valid_login():
    farm = farmOS.farmOS(**valid_credentials)
    success = farm.authenticate()

    assert success is True

def test_not_authenticated_exception_raised():
    with pytest.raises(NotAuthenticatedError):
        farm = farmOS.farmOS(**valid_credentials)
        farm.info()
