import os
import threading
import time
import typing

import httpx
import pytest
import uvicorn


async def app(scope: dict, receive: typing.Callable, send: typing.Callable) -> None:
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"]],
        }
    )
    await send({"type": "http.response.body", "body": b"Hello, world!"})


class TestServer(uvicorn.Server):
    def install_signal_handlers(self) -> None:
        pass

    @property
    def url(self) -> httpx.URL:
        return httpx.URL(f"http://{self.config.host}:{self.config.port}/")


def serve_in_thread(server: TestServer) -> typing.Iterator[TestServer]:
    thread = threading.Thread(target=server.run)
    thread.start()
    try:
        while not server.started:
            time.sleep(1e-3)
        yield server
    finally:
        server.should_exit = True
        thread.join()


@pytest.fixture(scope="session")
def uds_server():
    uds = "https_test_server.sock"
    config = uvicorn.Config(app=app, lifespan="off", uds=uds, loop="asyncio")
    server = TestServer(config=config)
    try:
        yield from serve_in_thread(server)
    finally:
        os.remove(uds)
