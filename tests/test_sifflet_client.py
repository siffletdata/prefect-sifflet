from pydantic import SecretStr

from prefect_sifflet.credentials import SiffletCredentials
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
