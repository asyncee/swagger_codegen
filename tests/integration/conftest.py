import contextlib
import socket
import sys
import tempfile
import threading
import time

import pytest
import uvicorn
from uvicorn import Config

from swagger_codegen.cli.main import generate

from .example_api import app


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()

    def url(self, path):
        return f"http://{self.config.host}:{self.config.port}{path}"


@pytest.fixture(scope="session")
def free_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    port = sock.getsockname()[1]
    sock.close()
    return port


@pytest.fixture(scope="session")
def server(free_port):
    config = Config(app, port=free_port)
    server = Server(config=config)

    with server.run_in_thread():
        yield server


@pytest.fixture(scope="session")
def example_api_client(server):
    tempdir = tempfile.mkdtemp()
    generate(uri=server.url("/openapi.json"), package="swclient", directory=tempdir)
    sys.path.append(tempdir)
    from swclient import Configuration, new_client

    from swagger_codegen.api.adapter.requests import RequestsAdapter

    yield new_client(RequestsAdapter(), Configuration(host=server.url("")))
