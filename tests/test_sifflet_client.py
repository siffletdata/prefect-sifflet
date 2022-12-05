import pytest
import responses
from pydantic import SecretStr

from prefect_sifflet.credentials import SiffletCredentials
from prefect_sifflet.exceptions import SiffletException
from prefect_sifflet.sifflet_client import SiffletClient


def test_client_construction():
    tenant = "tenant"
    api_token = "token"
    api_version = "v1"
    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))
    sc = SiffletClient(credentials=creds)

    expected_api_base_url = f"https://{tenant}api.siffletdata.com/api/{api_version}"

    assert sc.api_base_url == expected_api_base_url


def test_session_headers():
    tenant = "tenant"
    api_token = "token"

    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))
    sc = SiffletClient(credentials=creds)

    expected_headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_token}",
    }

    session = sc._get_session()

    assert session.headers == expected_headers


@responses.activate
def test_trigger_sifflet_rule_run_fail():
    tenant = "tenant"
    api_token = "token"
    api_version = "v1"
    rule_id = "id"

    expected_api_url = (
        f"https://{tenant}api.siffletdata.com/api/{api_version}/rules/{rule_id}/_run"
    )
    expected_error = "error"

    responses.add(
        method=responses.POST, url=expected_api_url, status=123, body=expected_error
    )

    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))
    sc = SiffletClient(credentials=creds)

    msg_match = f"Error while triggering rule run: {expected_error}"
    with pytest.raises(SiffletException, match=msg_match):
        sc.trigger_sifflet_rule_run(rule_id=rule_id)


@responses.activate
def test_trigger_sifflet_rule_run_succeed():
    tenant = "tenant"
    api_token = "token"
    api_version = "v1"
    rule_id = "id"

    expected_api_url = (
        f"https://{tenant}api.siffletdata.com/api/{api_version}/rules/{rule_id}/_run"
    )

    expected_json = {
        "id": "run_id",
        "createdDate": 0,
        "createdBy": "test",
        "startDate": 0,
        "endDate": 0,
        "result": "test",
        "status": "FAILED",
        "type": "MANUAL",
        "debugSql": "SELECT * FROM (Select 1) LIMIT 100",
        "ruleId": rule_id,
        "debuggable": True,
        "incidentStatus": "ONGOING",
        "incidentIssue": 1,
        "incidentName": " Sql Rule",
        "hasGroupBy": False,
    }

    responses.add(
        method=responses.POST, url=expected_api_url, status=200, json=expected_json
    )

    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))
    sc = SiffletClient(credentials=creds)

    response = sc.trigger_sifflet_rule_run(rule_id=rule_id)

    assert response == expected_json
    assert responses.calls[0].request.headers["Authorization"] == "Bearer token"


@responses.activate
def test_get_sifflet_rule_run_fail():
    tenant = "tenant"
    api_token = "token"
    api_version = "v1"
    rule_id = "id"
    rule_run_id = "run_id"

    expected_api_url = f"https://{tenant}api.siffletdata.com/api/{api_version}/rules/{rule_id}/runs?page=0&itemsPerPage=10&sort=createdDate%2CDESC"  # noqa

    responses.add(method=responses.GET, url=expected_api_url, status=123, body="error")
    expected_error = "error"

    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))
    sc = SiffletClient(credentials=creds)

    msg_match = f"Error while retrieving rule run: {expected_error}"
    with pytest.raises(SiffletException, match=msg_match):
        sc.get_sifflet_rule_run(rule_id=rule_id, rule_run_id=rule_run_id)


@responses.activate
def test_get_sifflet_rule_run_succeed():
    tenant = "tenant"
    api_token = "token"
    api_version = "v1"
    rule_id = "id"
    rule_run_id = "run_id_11"

    responses.add(
        method=responses.GET,
        url=f"https://{tenant}api.siffletdata.com/api/{api_version}/rules/{rule_id}/runs?page=0&itemsPerPage=10&sort=createdDate%2CDESC",  # noqa
        status=200,
        json={
            "totalElements": 12,
            "data": [{"id": f"run_id_{i}", "status": "FAILED"} for i in range(1, 11)],
        },
    )

    responses.add(
        method=responses.GET,
        url=f"https://{tenant}api.siffletdata.com/api/{api_version}/rules/{rule_id}/runs?page=1&itemsPerPage=10&sort=createdDate%2CDESC",  # noqa
        status=200,
        json={
            "totalElements": 12,
            "data": [
                {"id": "run_id_11", "status": "FAILED"},
                {"id": "run_id_12", "status": "FAILED"},
            ],
        },
    )

    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))
    sc = SiffletClient(credentials=creds)

    response = sc.get_sifflet_rule_run(rule_id=rule_id, rule_run_id=rule_run_id)

    assert response == {"id": "run_id_11", "status": "FAILED"}

    assert len(responses.calls) == 2
