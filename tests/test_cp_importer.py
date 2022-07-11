from typer.testing import CliRunner

from cp_importer import __version__
from cp_importer.main import app

runner = CliRunner()


def test_version():
    assert __version__ == "0.1.0"


def test_app():
    result = runner.invoke(app)
    assert result.exit_code == 0
