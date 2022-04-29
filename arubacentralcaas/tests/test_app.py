import json
import sys
from http import HTTPStatus
from pathlib import Path

import pytest
import typer
from typer.testing import CliRunner

sys.path.append(str(Path(".").absolute().parent))
from app import app

runner = CliRunner()


def test_show_accounts():
    result = runner.invoke(app, ["show-accounts"])
    assert result.exit_code == 0
    assert "central_info" in result.stdout


def test_show_gateways():
    result = runner.invoke(app, ["show-gateways", "--account", "tests"])
    assert result.exit_code == 0
    assert "Gateways" in result.stdout


# def test_show_routes():
#     result = runner.invoke(
#         app, ["show-routes", "aws-usw2-aruba-poc", "--account", "tests"]
#     )
#     assert result.exit_code == 0
#     assert "config" in result.stdout


def test_show_committed():
    result = runner.invoke(app, ["show-committed", "DDDD", "--account", "tests"])
    assert result.exit_code == 0
    assert "mcs" in result.stdout


def test_show_effective():
    result = runner.invoke(
        app, ["show-committed", "aws-usw2-aruba-poc", "--account", "tests"]
    )
    assert result.exit_code == 0
    assert "mcs" in result.stdout
