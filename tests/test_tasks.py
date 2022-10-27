from prefect import flow

from prefect_sifflet.tasks import (
    goodbye_prefect_sifflet,
    hello_prefect_sifflet,
)


def test_hello_prefect_sifflet():
    @flow
    def test_flow():
        return hello_prefect_sifflet()

    result = test_flow()
    assert result == "Hello, prefect-sifflet!"


def goodbye_hello_prefect_sifflet():
    @flow
    def test_flow():
        return goodbye_prefect_sifflet()

    result = test_flow()
    assert result == "Goodbye, prefect-sifflet!"
