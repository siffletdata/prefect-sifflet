import pytest
import responses
from prefect import flow

from prefect_sifflet.exceptions import SiffletException
from prefect_sifflet.tasks import get_sifflet_rule_run, trigger_sifflet_rule_run


@responses.activate
def test_get_sifflet_rule_run_fail():
    tenant = "tenant"
    api_token = "token"
    rule_id = "id"
    rule_run_id = "run_id"

    responses.add(
        method=responses.GET,
        url=f"https://{tenant}api.siffletdata.com/api/v1/rules/{rule_id}/runs/{rule_run_id}",  # noqa
        status=123,
    )

    @flow
    def test_flow():
        return get_sifflet_rule_run(
            tenant=tenant, api_token=api_token, rule_id=rule_id, rule_run_id=rule_run_id
        )

    with pytest.raises(SiffletException):
        test_flow()


def test_get_sifflet_rule_run_succeed():
    pass


@responses.activate
def test_trigger_sifflet_rule_run_fail():
    tenant = "tenant"
    api_token = "token"
    rule_id = "id"

    responses.add(
        method=responses.POST,
        url=f"https://{tenant}api.siffletdata.com/api/v1/rules/{rule_id}/_run",
        status=123,
    )

    @flow
    def test_flow():
        return trigger_sifflet_rule_run(
            tenant=tenant,
            api_token=api_token,
            rule_id=rule_id,
            wait_for_completion=False,
        )

    with pytest.raises(SiffletException):
        test_flow()


@responses.activate
def test_trigger_sifflet_rule_run_without_wait_succeed():
    tenant = "tenant"
    api_token = "token"
    rule_id = "id"
    rule_run_id = "run_id"

    responses.add(
        method=responses.POST,
        url=f"https://{tenant}api.siffletdata.com/api/v1/rules/{rule_id}/_run",
        status=200,
        json={"id": rule_run_id},
    )

    responses.add(
        method=responses.GET,
        url=f"https://{tenant}api.siffletdata.com/api/v1/rules/{rule_id}/runs/{rule_run_id}",  # noqa
        status=200,
        json={"id": rule_run_id, "status": "RUNNING"},
    )

    responses.add(
        method=responses.GET,
        url=f"https://{tenant}api.siffletdata.com/api/v1/rules/{rule_id}/runs/{rule_run_id}",  # noqa
        status=200,
        json={"id": rule_run_id, "status": "COMPLETED"},
    )

    @flow
    def test_flow():
        return trigger_sifflet_rule_run(
            tenant=tenant,
            api_token=api_token,
            rule_id=rule_id,
            wait_for_completion=True,
            wait_seconds_between_api_calls=1,
        )

    response = test_flow()

    assert response == {"id": rule_run_id, "status": "COMPLETED"}

    assert len(responses.calls) == 3


def test_trigger_sifflet_rule_run_with_wait_succeed():
    pass
