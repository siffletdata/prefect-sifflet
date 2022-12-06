import pytest
import responses
from prefect import flow

from prefect_sifflet.exceptions import SiffletException
from prefect_sifflet.tasks import get_sifflet_rule_run


@responses.activate
def test_get_sifflet_rule_run_fail():
    tenant = "tenant"
    api_token = "token"
    rule_id = "id"
    rule_run_id = "run_id"

    responses.add(
        method=responses.GET,
        url=f"https://{tenant}api.siffletdata.com/api/v1/rules/{rule_id}/runs?page=0&itemsPerPage=10&sort=createdDate%2CDESC",  # noqa
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


def test_trigger_sifflet_rule_run_fail():
    pass


def test_trigger_sifflet_rule_run_succeed():
    pass
