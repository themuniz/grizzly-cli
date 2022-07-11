# api.py
# Call the Grizzly API
# José Muñiz, School of Professional Studies, CUNY

import json

import requests

from .console import console

config = {}
with open("config.json") as file:
    try:
        config = json.load(file)
    except FileNotFoundError as e:
        console.log("No configuration file found.")


def get_token():
    url = config["api_url"]
    r = requests.post(
        url=f"{url}/login",
        data={"username": config["username"], "password": config["password"]},
        verify=False,
    )
    if r.raise_for_status():
        console.log("Error: We did not successfully login to API.")
        requests.exceptions.HTTPError()
    console.print_json(data=r.json(), ensure_ascii=False)
