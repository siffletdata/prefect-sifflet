from prefect_sifflet.blocks import SiffletCredentials


def test_credentials():
    expected_value = "the api token"
    creds = SiffletCredentials(api_token=expected_value)

    assert creds.api_token.get_secret_value() == expected_value
