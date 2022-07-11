import pytest
import requests
import cp_importer.lib.api as api


def test_get_token_invalid_credentials():
    with pytest.raises(requests.exceptions.HTTPError):
        api.get_token()
