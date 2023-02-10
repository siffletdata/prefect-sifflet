from pydantic import SecretStr

from prefect_sifflet.credentials import SiffletCredentials


def test_credentials():
    expected_tenant = "the tenant"
    expected_token = "the api token"
    creds = SiffletCredentials(
        tenant=expected_tenant, api_token=SecretStr(expected_token)
    )

    assert creds.tenant == expected_tenant
    assert creds.api_token.get_secret_value() == expected_token
