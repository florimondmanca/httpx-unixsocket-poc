# httpx-unixoscket-poc

Proof-of-concept for providing Unix Domain Socket (UDS) support for HTTPX as a third-party package.

**No maintenance intended.** But if you'd like to maintain an HTTPX UDS third-party package, please feel free to reuse as much of this code as you need. :-)

## Usage

This package provides a custom connection pool that connects to hosts via UDS instead of a regular TCP Internet socket.

As a real-world example, let's request the Docker API version through the Docker socket...

_**Hint**: try this code in IPython, or with Python 3.8+ with `python -m asyncio`._

```python
>>> import httpx
>>> from httpx_unixsocket_poc import UnixSocketConnectionPool
>>> dispatch = UnixSocketConnectionPool(uds="/var/run/docker.sock")
>>> async with httpx.AsyncClient(dispatch=dispatch) as client:
...     # This request will connect to the Docker API through the socket file.
...     response = await client.get("http://localhost/version")
...
>>> response.json()["Version"]
'19.03.2'
```

(If you get a `FileNotFoundError`, make sure that the Docker daemon is running.)

## Installation

Install from git:

```bash
pip install git+https://github.com/florimondmanca/httpx-unixsocket-poc
```

## Development notes

```bash
# Install dependencies
python -m venv venv
venv/bin/pip install -r requirements.txt

# Run the tests
venv/bin/pytest
```

## License

MIT
