from grizzly_cli import __version__

# from grizzly_cli.main import app


def test_version():
    assert __version__ == "0.1.0"


# def test_app():
#     result = runner.invoke(app)
#     assert result.exit_code == 0
