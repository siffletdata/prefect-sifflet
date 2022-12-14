"""
TODO
"""
from time import sleep
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
    Get information about a Sifflet Rule run given the rule identifier
    and the rule run identifier.

    Args:
        tenant: The tenant of the Sifflet deployment.
        api_token: The API token to use to authenticate API calls made to Sifflet.
        rule_id: The Sifflet Rule unique identifier.
        rule_run_id: The Sifflet Rule run unique identifier.

    Returns:
        An object with information about the requested rule run.
    """
    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))
    sc = SiffletClient(credentials=creds)

    return sc.get_sifflet_rule_run(rule_id=rule_id, rule_run_id=rule_run_id)


@task
def trigger_sifflet_rule_run(
    tenant: str,
    api_token: str,
    rule_id: str,
    wait_for_completion: bool = True,
    wait_seconds_between_api_calls: int = 10,
) -> Dict:
    """
    Trigger a Sifflet Rule run and optionally wait for its completion.

    Args:
        tenant: The tenant of the Sifflet deployment.
        api_token: The API token to use to authenticate API calls made to Sifflet.
        rule_id: The Sifflet Rule unique identifier.
        wait_for_completion: Whether to wait for the rule run to complete or not.
        wait_seconds_between_api_calls: THe number of seconds to wait between API calls
            made to retrieve the rule run status.

    Returns:
        If `wait_for_completion` is `True`, then returns an object with information
            about the triggered run. Otherwise, returns information about
            the completed rule run.
    """
    creds = SiffletCredentials(tenant=tenant, api_token=SecretStr(api_token))
    sc = SiffletClient(credentials=creds)

    if wait_for_completion:
        trigger_rule_run_response = sc.trigger_sifflet_rule_run(rule_id=rule_id)
        rule_run_id = trigger_rule_run_response["id"]

        while True:
            rule_run_response = sc.get_sifflet_rule_run(
                rule_id=rule_id, rule_run_id=rule_run_id
            )
            rule_run_status = rule_run_response["status"]
            if rule_run_status != "RUNNING":
                return rule_run_response

            sleep(wait_seconds_between_api_calls)

    else:
        return sc.trigger_sifflet_rule_run(rule_id=rule_id)
