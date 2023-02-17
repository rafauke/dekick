from logging import basicConfig, debug
from os import environ, getcwd, path, remove
from os.path import exists
from time import sleep

import pytest
from filelock import SoftFileLock

from lib.tests.boilerplates import copy_flavour_to_container, download_boilerplates
from lib.tests.dind import start_dind_container, stop_dind_container
from lib.tests.misc import parse_flavour_version
from lib.tests.registry import start_docker_registry


def pytest_configure(config):
    worker_id = environ.get("PYTEST_XDIST_WORKER")
    if worker_id is not None:
        basicConfig(
            format=config.getini("log_file_format"),
            filename=f"logs/pytest_{worker_id}.log",
            level=config.getini("log_file_level"),
        )


def init_session():
    """Do some things before workers start"""
    lock_path = "tmp/pytest.lock"
    worker_id = environ.get("PYTEST_XDIST_WORKER")
    debug("worker_id: %s", worker_id)

    if worker_id in ("gw0", "master"):
        if exists(lock_path):
            remove(lock_path)

        with SoftFileLock(lock_path):
            start_docker_registry()
            download_boilerplates()
            return

    sleep(1)
    lock = SoftFileLock(lock_path, timeout=240)
    lock.acquire(poll_interval=1)
    debug("Lock acquired, let's move!")
    return


@pytest.fixture(scope="session", autouse=True)
def start_session(request):
    """Setup boilerplates before running tests"""
    debug("start session")
    init_session()
    request.addfinalizer(teardown_session)


def teardown_session():
    """Teardown boilerplates after running tests"""
    pass


@pytest.fixture(scope="function", autouse=True)
def start_function(request):
    """Cleans up boilerplates and stops containers before running test"""
    container_id = start_dind_container()
    copy_flavour_to_container(
        *parse_flavour_version(path.basename(request.node.fspath)),
        container_id=container_id,
    )
    request.addfinalizer(teardown_function)


def teardown_function():
    """Cleans up boilerplates and stops containers after running test"""
    stop_dind_container()
