import httpx
import pytest

from farmOS import AsyncFarmClient

HOST = "http://farm.test"


def _error_transport(status):
    def handler(request):
        return httpx.Response(status, json={"errors": [{"status": str(status)}]})

    return httpx.MockTransport(handler)


@pytest.mark.anyio
async def test_get_raises_on_http_error():
    async with AsyncFarmClient(HOST, transport=_error_transport(500)) as farm:
        with pytest.raises(httpx.HTTPStatusError):
            await farm.resource.get("log", "observation")


@pytest.mark.anyio
async def test_send_raises_on_http_error():
    async with AsyncFarmClient(HOST, transport=_error_transport(422)) as farm:
        with pytest.raises(httpx.HTTPStatusError):
            await farm.resource.send(
                "log", "observation", {"attributes": {"name": "x"}}
            )


@pytest.mark.anyio
async def test_delete_raises_on_http_error():
    async with AsyncFarmClient(HOST, transport=_error_transport(404)) as farm:
        with pytest.raises(httpx.HTTPStatusError):
            await farm.resource.delete("log", "observation", "missing-id")


@pytest.mark.anyio
async def test_info_raises_on_http_error():
    async with AsyncFarmClient(HOST, transport=_error_transport(503)) as farm:
        with pytest.raises(httpx.HTTPStatusError):
            await farm.info()
