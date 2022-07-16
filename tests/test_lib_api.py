import pytest
import requests
import grizzly_cli.lib.api as api


def test_get_token_invalid_credentials():
    with pytest.raises(requests.exceptions.HTTPError):
        api.get_token()
