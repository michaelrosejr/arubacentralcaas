import sys
from pathlib import Path

sys.path.append(str(Path(".").absolute().parent))
from app import app  # noqa: E402
from typer.testing import CliRunner  # noqa: E402

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
