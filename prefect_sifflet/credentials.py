"""
Block that holds information required to connect to the Sifflet platform.
"""

from prefect.blocks.core import Block
from pydantic import SecretStr


class SiffletCredentials(Block):
    """
    A block that holds information required to connect to the Sifflet platform.

    Attributes:
        tenant (Field): The tenant of the Sifflet deployment
        api_token (SecretStr): The API token to use to interact with Sifflet.

    Example:
        Load a stored value:
        ```python
        from prefect_sifflet import SiffletCredentials
        block = SiffletCredentials.load("BLOCK_NAME")
        ```
    """

    tenant: str
    api_token: SecretStr

    _block_type_name = "Sifflect Credentials"
    # _logo_url = "https://path/to/logo.png"
