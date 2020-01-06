import asyncio
import functools
import ssl
import typing

import httpx
import sniffio
from httpx.backends.asyncio import SocketStream
from httpx.backends.base import BaseSocketStream
from httpx.dispatch.connection import HTTPConnection
from httpx.dispatch.connection_pool import ConnectionPool


async def open_uds_socket_stream(
    path: str, hostname: str, timeout: httpx.Timeout, ssl_context: ssl.SSLContext = None
) -> BaseSocketStream:
    async_library = sniffio.current_async_library()
    assert async_library == "asyncio"

    server_hostname = hostname if ssl_context else None

    try:
        stream_reader, stream_writer = await asyncio.wait_for(
            asyncio.open_unix_connection(
                path, ssl=ssl_context, server_hostname=server_hostname
            ),
            timeout.connect_timeout,
        )
    except asyncio.TimeoutError:
        raise httpx.ConnectTimeout()

    return SocketStream(stream_reader=stream_reader, stream_writer=stream_writer)


class UnixSocketHTTPConnection(HTTPConnection):
    def __init__(self, *, uds: str, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.uds = uds

    async def open_socket_stream(
        self,
        origin: httpx.Origin,
        timeout: httpx.Timeout,
        ssl_context: ssl.SSLContext = None,
    ) -> BaseSocketStream:
        path = self.uds
        host = origin.host
        self.logger.trace(
            f"start_connect uds path={path!r} host={host!r} timeout={timeout!r}"
        )
        return await open_uds_socket_stream(
            path=path, hostname=host, timeout=timeout, ssl_context=ssl_context
        )


class UnixSocketConnectionPool(ConnectionPool):
    def __init__(self, *, uds: str, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self.uds = uds

    def get_connection_factory(self) -> typing.Callable[..., HTTPConnection]:
        return functools.partial(UnixSocketHTTPConnection, uds=self.uds)
