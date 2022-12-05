"""
TODO
"""
from typing import Dict

from requests import Session

from .credentials import SiffletCredentials
from .exceptions import SiffletException


class SiffletClient:
    """
    TODO
    """

    def __init__(self, credentials: SiffletCredentials) -> None:
        """
        TODO
        """
        self.credentials = credentials
        self.api_version = "v1"
        self.api_base_url = (
            f"https://{credentials.tenant}api.siffletdata.com/api/{self.api_version}"
        )

    def _get_session(self) -> Session:
        """
        TODO
        """
        session = Session()
        session.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.credentials.api_token.get_secret_value()}",
        }

        return session

    def _get_trigger_sifflet_run_api_url(self, rule_id: str) -> str:
        """
        TODO
        """
        return f"{self.api_base_url}/rules/{rule_id}/_run"

    def _get_sifflet_rule_runs_api_url(
        self,
        rule_id: str,
        page_id: int,
        items_per_page: int,
        sort_key: str,
        sort_desc: bool = True,
    ) -> str:
        """
        TODO
        """
        sort_direction = "DESC" if sort_desc else "ASC"
        return f"{self.api_base_url}/rules/{rule_id}/runs?page={page_id}&itemsPerPage={items_per_page}&sort={sort_key}%2C{sort_direction}"  # noqa

    def trigger_sifflet_rule_run(self, rule_id: str) -> Dict:
        """
        TODO
        """
        url = self._get_trigger_sifflet_run_api_url(rule_id=rule_id)
        session = self._get_session()

        with session.post(url=url) as response:
            if response.status_code != 200:
                raise SiffletException(
                    f"Error while triggering rule run: {response.text}"
                )
            else:
                return response.json()

    def get_sifflet_rule_run(self, rule_id: str, rule_run_id: str) -> Dict:
        """
        TODO
        """
        current_page_id = 0
        items_per_page = 10

        while True:
            url = url = self._get_sifflet_rule_runs_api_url(
                rule_id=rule_id,
                page_id=current_page_id,
                items_per_page=items_per_page,
                sort_key="createdDate",
            )
            session = self._get_session()
            with session.get(url=url) as response:
                if response.status_code != 200:
                    raise SiffletException(
                        f"Error while retrieving rule run: {response.text}"
                    )

                r = response.json()
                rule_runs = r["data"]
                total_runs = r["totalElements"]
                for rule_run in rule_runs:
                    if rule_run["id"] == rule_run_id:
                        return rule_run

                if total_runs // items_per_page > current_page_id:
                    current_page_id += 1
                else:
                    break

        err_msg = f"Sifflet rule run not found! Rule ID: {rule_id}, Rule Run ID: {rule_run_id}"  # noqa
        raise SiffletException(err_msg)
