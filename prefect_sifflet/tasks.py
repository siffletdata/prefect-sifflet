"""
TODO
"""
from typing import Dict

from prefect import task
from pydantic import SecretStr

from prefect_sifflet.credentials import SiffletCredentials
from prefect_sifflet.sifflet_client import SiffletClient


@task
def get_sifflet_rule_run(
    tenant: str, api_token: str, rule_id: str, rule_run_id: str
) -> Dict:
    """
    TODO
    """
    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))

    sc = SiffletClient(credentials=creds)

    return sc.get_sifflet_rule_run(rule_id=rule_id, rule_run_id=rule_run_id)


@task
def trigger_sifflet_rule_run(
    tenant: str, api_token: str, rule_id: str, wait_for_completion: bool = True
) -> Dict:
    """
    TODO
    """
    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))

    sc = SiffletClient(credentials=creds)

    if wait_for_completion:
        trigger_response = sc.trigger_sifflet_rule_run(rule_id=rule_id)
        rule_run_id = trigger_response["id"]
        while True:
            get_rule_run_response = sc.get_sifflet_rule_run(
                rule_id=rule_id, rule_run_id=rule_run_id
            )
            rule_run_status = get_rule_run_response["status"]
            if rule_run_status != "RUNNING":
                return get_rule_run_response

    else:
        return sc.trigger_sifflet_rule_run(rule_id=rule_id)
