"""This is an example flows module"""
from prefect import flow

from prefect_sifflet.blocks import SiffletBlock
from prefect_sifflet.tasks import (
    goodbye_prefect_sifflet,
    hello_prefect_sifflet,
)


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    SiffletBlock.seed_value_for_example()
    block = SiffletBlock.load("sample-block")

    print(hello_prefect_sifflet())
    print(f"The block's value: {block.value}")
    print(goodbye_prefect_sifflet())
    return "Done"


if __name__ == "__main__":
    hello_and_goodbye()
