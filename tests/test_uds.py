import httpx
import pytest
import uvicorn

from httpx_unixsocket_poc import UnixSocketConnectionPool


@pytest.mark.asyncio
async def test_uds(uds_server: uvicorn.Server) -> None:
    url = uds_server.url
    uds = uds_server.config.uds
    assert uds is not None

    dispatch = UnixSocketConnectionPool(uds=uds)
    async with httpx.AsyncClient(dispatch=dispatch) as client:
        response = await client.get(url)

    assert response.status_code == 200
    assert response.text == "Hello, world!"
    assert response.encoding == "iso-8859-1"
