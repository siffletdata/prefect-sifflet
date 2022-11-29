"""This is an example blocks module"""

from prefect.blocks.core import Block
from pydantic import SecretStr


class SiffletCredentials(Block):
    """
    A block that holds a Sifflet API token.

    Attributes:
        api_token (SecretStr): The API token to use to interact with Sifflet.

    Example:
        Load a stored value:
        ```python
        from prefect_sifflet import SiffletCredentials
        block = SiffletBlock.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "sifflet"
    # _logo_url = "https://path/to/logo.png"

    api_token = SecretStr("The API token value")
