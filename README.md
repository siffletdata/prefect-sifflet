# prefect-sifflet

<p align="center">
    <a href="https://pypi.python.org/pypi/prefect-sifflet/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/prefect-sifflet?color=0052FF&labelColor=090422"></a>
    <a href="https://github.com/Siffletapp/prefect-sifflet/" alt="Stars">
        <img src="https://img.shields.io/github/stars/Siffletapp/prefect-sifflet?color=0052FF&labelColor=090422" /></a>
    <a href="https://pepy.tech/badge/prefect-sifflet/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/prefect-sifflet?color=0052FF&labelColor=090422" /></a>
    <a href="https://github.com/Siffletapp/prefect-sifflet/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/Siffletapp/prefect-sifflet?color=0052FF&labelColor=090422" /></a>
    <br>
    <a href="https://prefect-community.slack.com" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" /></a>
    <a href="https://discourse.prefect.io/" alt="Discourse">
        <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?color=0052FF&labelColor=090422&logo=discourse" /></a>
</p>

## Welcome!

Integrate Sifflet Data Observability Platform with Prefect

## Getting Started

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://orion-docs.prefect.io/).

### Installation

Install `prefect-sifflet` with `pip`:

```bash
pip install prefect-sifflet
```

Then, register to [view the block](https://orion-docs.prefect.io/ui/blocks/) on Prefect Cloud:

```bash
prefect block register -m prefect_sifflet.credentials
```

Note, to use the `load` method on Blocks, you must already have a block document [saved through code](https://orion-docs.prefect.io/concepts/blocks/#saving-blocks) or [saved through the UI](https://orion-docs.prefect.io/ui/blocks/).

### Write and run a flow

```python
from prefect import flow
from prefect_sifflet.tasks import (
    trigger_sifflet_rule_run,
    get_sifflet_rule_run,
)


@flow
def execute_rule():
    tenant = "<your tenant>"
    api_token = "<your API token>"
    rule_id = "<your rule ID>"

    response = trigger_sifflet_rule_run(
        tenant=tenant,
        api_token=api_token,
        rule_id=rule_id,
        wait_for_completion=False
    )
    rule_run_id = response["id"]

    rule_run_result = get_sifflet_rule_run(
        tenant=tenant,
        api_token=api_token,
        rule_id=rule_id,
        rule_run_id=rule_run_id
    )

execute_rule()
```

## Resources

If you encounter any bugs while using `prefect-sifflet`, feel free to open an issue in the [prefect-sifflet](https://github.com/Siffletapp/prefect-sifflet) repository.

If you have any questions or issues while using `prefect-sifflet`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

Feel free to ⭐️ or watch [`prefect-sifflet`](https://github.com/Siffletapp/prefect-sifflet) for updates too!

## Development

If you'd like to install a version of `prefect-sifflet` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/Siffletapp/prefect-sifflet.git

cd prefect-sifflet/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
