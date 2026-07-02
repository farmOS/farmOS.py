import httpx
import pytest

from farmOS import FarmClient

HOST = "http://farm.test"


def _error_transport(status):
    def handler(request):
        return httpx.Response(status, json={"errors": [{"status": str(status)}]})

    return httpx.MockTransport(handler)



def test_get_raises_on_http_error():
    with FarmClient(HOST, transport=_error_transport(500)) as farm:
        with pytest.raises(httpx.HTTPStatusError):
            farm.resource.get("log", "observation")



def test_send_raises_on_http_error():
    with FarmClient(HOST, transport=_error_transport(422)) as farm:
        with pytest.raises(httpx.HTTPStatusError):
            farm.resource.send("log", "observation", {"attributes": {"name": "x"}})



def test_delete_raises_on_http_error():
    with FarmClient(HOST, transport=_error_transport(404)) as farm:
        with pytest.raises(httpx.HTTPStatusError):
            farm.resource.delete("log", "observation", "missing-id")



def test_info_raises_on_http_error():
    with FarmClient(HOST, transport=_error_transport(503)) as farm:
        with pytest.raises(httpx.HTTPStatusError):
            farm.info()
